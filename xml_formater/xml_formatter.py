def set_params(params=None):
    if not params:
        params = {'use_tab': False, 'smart_tabs': False, 'tab_size': 4, 'indent': 4, 'continuation_indent': 8,
                  'keep_indents_on_empty_line': False, 'keep_line_breaks': True, 'keep_line_breaks_in_text': True,
                  'keep_blank_lines': 2, 'wrap_attrs': 1, 'wrap_text': True, 'align_attrs': True,
                  'keep_white_spaces': False, 'space_around_equal': False, 'space_after_tag_name': False,
                  'space_in_empty_tag': False}
        # wrap attrs :  0 - do not wrap / 1 - wrap if long / 2 - chop down if long / 3 - wrap always
    return params


def format(info, params=None):
    params = set_params(params)
    indent_char = "\t" if params['use_tab'] else ' '
    result = ''
    for tag in info:
        # print(tag)
        if tag['type'] == 'text':
            text = format_text(params, tag['name'], indent_char, tag['level'], get_last_string_length(result))
            result += text
        elif tag['type'] == 'opening':
            result += get_indent(params, indent_char, tag['level']) + '<' + tag['name'] + format_attrs(params, tag, indent_char) + format_space_in_tag(params) + '>'
        elif tag['type'] == 'closing':
            if (not params['keep_white_spaces']) and only_spaces_in_last_line(result):  # if closing tag starts on new line we need to add indent
                while result[-1] != "\n":  # but if there are spaces we need to remove it to add correct indent
                    result = result[:-1]
                result += get_indent(params, indent_char, tag['level'])
            result += '<' + tag['name'] + format_space_in_tag(params) + '>'
        elif tag['type'] == 'opening-closing':
            result += get_indent(params, indent_char, tag['level']) + '<' + tag['name'] + format_attrs(params, tag, indent_char) + format_space_in_tag(params, True) + '/>'

    if not params['keep_white_spaces']:
        result = remove_blank_lines(result, params)

    result = result.expandtabs(params['tab_size'])

    return result


def only_spaces_in_last_line(text):
    last_line = text.split("\n")[-1]
    return last_line == '' or last_line.isspace()


def remove_blank_lines(result, params):
    i = len(result) - 1
    blank_lines_count = 0
    while i >= 0:
        if result[i] != "\n" and result[i] != "\t" and result[i] != ' ':
            blank_lines_count = 0
        if result[i] == "\n":
            blank_lines_count += 1
        if blank_lines_count > params['keep_blank_lines'] + 1:
            index = i + 1
            while result[index] != "\n":
                index += 1
            result = result[0:i] + result[index:]
            blank_lines_count -= 1
        i -= 1
    return result


def get_indent(params, indent_char, level):
    return indent_char * (level * params['indent']) if not params['keep_white_spaces'] else ''


def format_space_in_tag(params, empty=False):
    return ' ' if params['space_after_tag_name'] or (empty and params['space_in_empty_tag']) else ''


def format_attrs(params, tag, indent_char):
    attrs = tag.get('attrs', None)
    if not attrs:
        return ''

    result = ''
    if params['wrap_attrs'] == 3:
        result = chop_down_every_attr(attrs, params, indent_char, tag)
    elif params['keep_line_breaks'] and len(attrs) > 1:
        for i, attr in enumerate(attrs):
            use_cont_indent = use_continuation_indent(attrs)
            if (i > 0 and attrs[i-1]['value'][-1] == "\n") or use_cont_indent:
                if i == 0 and use_cont_indent:
                    result += "\n"
                result += get_indent_for_attr(params, indent_char, tag['name'], tag['level'], use_cont_indent)
            if not use_cont_indent:
                result += ' '
            result += attr['name'] + format_equal(params) + attr['value']
    else:
        for attr in attrs:
            while attr['value'][-1] == "\n":
                attr['value'] = attr['value'][:-1]
            result += ' ' + attr['name'] + format_equal(params) + attr['value']

    line_beg = get_indent(params, indent_char, tag['level']) + '<' + tag['name']
    full_line = line_beg + result + '>'
    if attr_line_too_long(full_line):
        if params['wrap_attrs'] == 2:
            result = chop_down_every_attr(attrs, params, indent_char, tag)
        elif params['wrap_attrs'] == 1:
            result = format_long_string(result, 120, len(line_beg), True, params, indent_char, tag['name'], tag['level'], use_continuation_indent(attrs))

    return result


def use_continuation_indent(attrs):
    return True if attrs[0]['new_line'] else False


def attr_line_too_long(attrs_lines):
    for line in attrs_lines.split("\n"):
        if len(line) > 120:
            return True
    return False


def chop_down_every_attr(attrs, params, indent_char, tag):
    result = ''
    for i, attr in enumerate(attrs):
        while attr['value'][-1] == "\n":
            attr['value'] = attr['value'][:-1]
        if i != 0:
            result += get_indent_for_attr(params, indent_char, tag['name'], tag['level'], use_continuation_indent(attrs))
        result += ' ' + attr['name'] + format_equal(params) + attr['value']
        if i != len(attrs) - 1:
            result += "\n"
    return result


def get_indent_for_attr(params, indent_char, tag_name, level, use_cont_indent=False):
    result = get_indent(params, indent_char, level)
    if use_cont_indent:
        if params['use_tab']:
            tab_count = (params['continuation_indent'] / params['tab_size'])
            space_count = params['continuation_indent'] - tab_count*params['tab_size']
            result += "\t" * tab_count + ' '*space_count
        else:
            result += ' ' * params['continuation_indent']
    elif params['align_attrs']:
        if params['use_tab'] and not params['smart_tabs']:
            result += "\t" * ((len(tag_name) + 1) / params['tab_size'])
        else:
            result += ' ' * (len(tag_name) + 1)
    else:
        result += indent_char * params['indent']
    return result


def format_equal(params):
    return " = " if params['space_around_equal'] else "="


def format_long_string(text, length, beg_length, attr=False, params=None, indent_char=None, tag_name=None, level=None, use_cont_indent=False):
    wrapped_text = False
    do_not_check = []  # to store indexes of lines that cannot be split
    while not wrapped_text:
        new_text = ''
        wrapped_text = True
        first = True
        i = 0
        for line in text.split("\n"):
            if i in do_not_check:  # dont need to try to split string without spaces
                new_text += line  # but need to add whole string to result
                if len(text.split("\n")) > 1:
                    new_text += "\n"
                continue
            new_length = length - beg_length if first else length
            first = False
            if len(line) > new_length:
                wrapped_text = False
                index = line[0:new_length].rfind(' ')
                if index == -1:
                    index = line[new_length:].find(' ')
                    if index == -1:  # no spaces in string
                        do_not_check.append(i)
                        index = 0
                        line = ' ' + line  # first char will be deleted
                if attr:
                    line = line[:index] + "\n " + get_indent_for_attr(params, indent_char, tag_name, level, use_cont_indent) + line[index + 1:]
                else:
                    line = line[:index] + "\n" + line[index + 1:]
            else:
                first = False

            i += 1
            new_text += line
            if len(text.split("\n")) > 1:
                new_text += "\n"

        if new_text.endswith("\n"):
            new_text = new_text[:-1]

        text = new_text
    return text


def format_text(params, text, indent_char, level, length):
    if not params['keep_white_spaces']:
        if (not params['keep_line_breaks_in_text']) and (not text.isspace()):
            text = text.replace("\n", '')
        if not (params['keep_indents_on_empty_line'] and text.isspace() and text.count("\n") > 1):
            while text and (text[0] == ' ' or text[0] == "\t"):  # remove whitespaces from the beginning
                text = text[1:]
            while text[-1:] == ' ' or text[-1:] == "\t":  # remove whitespaces from the end
                text = text[:-1]
            while text.find("\n ") >= 0:
                text = text.replace("\n ", "\n")
            while text.find("\n\t") >= 0:
                text = text.replace("\n\t", "\n")

        if not text.isspace():
            if params['wrap_text']:
                text = format_long_string(text, 120 - level * params['indent'], length)

            text = text.replace("\n", ("\n" + get_indent(params, indent_char, level)))  # add indent fot text
            if text.find("\n") >= 0 and (not only_spaces_in_last_line(text)):  # put closing tag in new line
                text += "\n"

    return text


def get_last_string_length(text):
    return len(text.split("\n")[-1])

def set_params(default=True):
    params = {'use_tab': False, 'indent': 4, 'keep_line_breaks': True, 'keep_blank_lines': 2,
              'wrap_attr': 'long', 'wrap_text': True}
    if default:
        return params


def format(info):
    params = set_params()
    indent_char = "\t" if params['use_tab'] else ' '
    result = ''
    for tag in info:
        # print(tag)
        if tag['type'] == 'text':
            text = format_text(params, tag['name'], indent_char, tag['level'])
            result += text

        elif tag['type'] == 'opening':
            result += get_indent(params, indent_char, tag['level']) + '<' + tag['name'] + format_attrs(params, tag, indent_char) + '>'
        elif tag['type'] == 'closing':
            if result[-1:] == "\n":
                result += get_indent(params, indent_char, tag['level'])
            result += '<' + tag['name'] + '>'
        elif tag['type'] == 'opening-closing':
            result += get_indent(params, indent_char, tag['level']) + '<' + tag['name'] + format_attrs(params, tag, indent_char) + '/>'

        result = "\n".join(str(x) for x in result.split("\n") if not x.isspace())  # remove whitespaces from blank line

        while result[(-1*(params['keep_blank_lines']+2)):] == ("\n" * (params['keep_blank_lines']+2)):
            result = result[:-1]

    return result


def get_indent(params, indent_char, level):
    return indent_char * (level * params['indent'])


def format_attrs(params, tag, indent_char):
    attrs = tag.get('attrs', None)
    if not attrs:
        return ''

    result = ''
    if params['keep_line_breaks'] and len(attrs) > 1:
        for i, attr in enumerate(attrs):
            if i > 0 and attrs[i-1]['value'][-1] == "\n":
                result += get_indent(params, indent_char, tag['level']) + ' '*(len(tag['name']) + 1)
            result += ' ' + attr['name'] + '=' + attr['value']
    else:
        for attr in attrs:
            while attr['value'][-1] == "\n":
                attr['value'] = attr['value'][:-1]
            result += ' ' + attr['name'] + '=' + attr['value']

    return result


def format_long_string(text, length):
    wrapped_text = False
    while not wrapped_text:
        new_text = ''
        wrapped_text = True
        for line in text.split("\n"):
            if len(line) > length:
                wrapped_text = False
                index = length
                while index > 0:
                    if line[index] == ' ':
                        line = line[:index] + "\n" + line[index + 1:]
                        break
                    index -= 1
            new_text += line
            if len(text.split("\n")) > 1:
                new_text += "\n"
        text = new_text
    return text


def format_text(params, text, indent_char, level):
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
            text = format_long_string(text, 120 - level * params['indent'])

        text = text.replace("\n", ("\n" + get_indent(params, indent_char, level)))  # add indent fot text
        if text.find("\n") >= 0 and text[-1] != "\n":  # put closing tag in new line
            text += "\n"

    return text

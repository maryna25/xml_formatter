def analyze(path):
    """Function for analyzing xml"""

    file = open(path)
    line = file.read()

    tags = []  # stack to check if all tags are closed
    info = []  # array with all tags
    errors = []  # array with all errors
    index = 1  # line number
    tag_name = ''  # tag name
    tag_type = 'opening'  # opening closing opening-closing
    quote_char = '"'  # opening quote for attribute value
    attr_name = ''  # attribute name
    attr_value = ''  # attribute value
    xml_tag = False  # True if tag is <?xml ... ?>
    level = 0
    text = ''
    new_line = False

    state = ''  # start_name name after_name closing_expected text attr_name quote_expected attr_value whitespace_expected

    for ch in line:
        # print(state, ch)
        if ch == "\n":
            index += 1
        if state == '':
            if ch == ' ' or ch == "\t" or ch == "\n":
                text += ch
            elif ch == '<':
                info.append({'name': text, 'level': level, 'type': 'text', 'value': ''})
                text = ''
                state = 'start_name'
                tag_type = 'opening'
            else:
                text += ch
                errors.append({index: 'Content is not allowed in prolog'})
        elif state == 'start_name':
            tag_name = ''
            if ch == ' ' or ch == "\t" or ch == "\n":
                continue
            elif ch == '/':
                if len(tags) > 0:
                    tag_type = 'closing'
                else:
                    errors.append({index: 'Invalid tag name'})
            elif ch.isalpha() or ch == '_':
                state = 'name'
                tag_name += ch
            elif index == 1 and ch == '?':
                tag_name += ch
                state = 'name'
                xml_tag = True
            else:
                errors.append({index: 'Invalid tag name'})
        elif state == 'name':
            if ch.isalpha() or ch.isdigit() or ch == '.' or ch == '-' or ch == '_':
                tag_name += ch
            elif ch == '/':
                state = 'closing_expected'
                if tag_type == 'opening':
                    tag_type = 'opening-closing'
                    info.append({'name': tag_name, 'level': level, 'type': 'opening-closing', 'value': ''})
                    state = 'closing_expected'
                else:
                    errors.append({index: 'Invalid tag name'})
            elif ch == ' ' or ch == "\t" or ch == "\n":
                if ch == "\n":
                    new_line = True
                state = 'after_name'
                if tag_type == 'opening':
                    info.append({'name': tag_name, 'level': level, 'type': 'opening', 'value': ''})
                    if tag_name != '?xml':
                        tags.append(tag_name)
                        level += 1
                elif tag_type == 'closing':
                    if tags[-1] != tag_name:
                        errors.append({index: 'Unmatched closing tag: ' + tag_name})
                    tags.pop()
                    level -= 1
                    info.append({'name': '/' + tag_name, 'level': level, 'type': 'closing', 'value': ''})
            elif ch == '>':
                state = 'text'
                if tag_type == 'opening':
                    info.append({'name': tag_name, 'level': level, 'type': 'opening', 'value': ''})
                    if tag_name != '?xml':
                        tags.append(tag_name)
                        level += 1
                elif tag_type == 'closing':
                    if tags[-1] != tag_name:
                        errors.append({index: 'Unmatched closing tag: ' + tag_name})
                    tags.pop()
                    level -= 1
                    info.append({'name': '/' + tag_name, 'level': level, 'type': 'closing', 'value': ''})
            else:
                errors.append({index: 'Invalid tag name'})
        elif state == 'after_name':
            if ch == ' ' or ch == "\t" or ch == "\n":
                if ch == "\n":
                    new_line = True
                continue
            if ch == '/':
                state = 'closing_expected'
                if tag_type == 'opening':
                    tag_type = 'opening-closing'
                    state = 'closing_expected'
                else:
                    errors.append({index: 'Invalid tag name'})
            elif ch == '>':
                state = 'text'
            elif ch.isalpha() or ch == '_':
                state = 'attr_name'
                attr_name += ch
            elif ch == '<':
                state = 'start_name'
                errors.append({index: 'Unclosed tag'})
            else:
                errors.append({index: 'Invalid attribute name'})
        elif state == 'closing_expected':
            if ch == '>':
                state = 'text'
            else:
                errors.append({index: 'Closing tag was expected'})
        elif state == 'text':
            if ch == '<':
                info.append({'name': text, 'level': level, 'type': 'text', 'value': ''})
                text = ''
                state = 'start_name'
                tag_type = 'opening'
            else:
                text += ch
        elif state == 'attr_name':
            if ch.isalpha() or ch.isdigit() or ch == '.' or ch == '-' or ch == '_' or ch == ' ' or ch == "\t" or ch == "\n":
                attr_name += ch
            elif ch == '=':
                if attr_name[0:4] == 'xml:':
                    errors.pop()
                if attr_name == 'xml':
                    errors.append({index: 'xml cannot be attribute name'})
                state = 'quote_expected'
            elif ch == '>':
                state = 'text'
                errors.append({index: 'Attribute must be followed by ='})
            else:
                attr_name += ch
                errors.append({index: 'Invalid attribute name'})
        elif state == 'quote_expected':
            if ch == ' ' or ch == "\t" or ch == "\n":
                continue
            elif ch == '"' or ch == "'":
                quote_char = ch
                state = 'attr_value'
            else:
                quote_char = None
                state = 'attr_value'
                attr_value += ch
                errors.append({index: 'Quote is expected'})
            attr_value = ''
        elif state == 'attr_value':
            if ch == quote_char:
                state = 'whitespace_expected'
                attr_value = quote_char + attr_value + quote_char
                info.append({'name': attr_name, 'level': level, 'type': 'attr', 'value': attr_value, 'new_line': new_line})
                new_line = False
                attr_name = ''
                attr_value = ''
            if not quote_char:
                if ch == '>':
                    state = 'text'
                elif ch == '/':
                    if tag_type == 'opening':
                        tag_type = 'opening-closing'
                        state = 'closing_expected'
                    else:
                        errors.append({index: 'Invalid tag'})
                elif ch == ' ' or ch == "\t" or ch == "\n":
                    if ch == "\n":
                        new_line = True
                    state = 'after_name'
                else:
                    attr_value += ch
            else:
                attr_value += ch
        elif state == 'whitespace_expected':
            if ch == '>':
                state = 'text'
            elif ch == '/':
                if tag_type == 'opening':
                    tag_type = 'opening-closing'
                    state = 'closing_expected'
                else:
                    errors.append({index: 'Invalid tag'})
            elif ch == ' ' or ch == "\t" or ch == "\n":
                if ch == "\n":
                    info[-1]['value'] += "\n"
                    new_line = True
                state = 'after_name'
            elif xml_tag and ch == '?':
                state = 'closing_expected'
            else:
                errors.append({index: 'Invalid tag'})

    if state != 'text':
        errors.append({index: 'XML is not valid'})
    if len(tags) > 0:
        errors.append({index: '"' + ','.join(tags) + '" tags are not closed'})

    # print(tags)
    # print(errors)
    # print(info)
    # print(state)

    return unique(errors), add_attrs_to_tag(info)


def add_attrs_to_tag(info):
    """Function for adding attributes (attr_name and value) to tag"""

    attrs = []
    index = 0
    for el in info[:]:
        if el['type'] == 'attr':
            attrs.append({'name': el['name'], 'value': el['value'], 'new_line': el['new_line']})
            info.remove(el)
        else:
            if len(attrs) > 0:
                info[index-1]['attrs'] = attrs
                attrs = []
            index += 1
    return info


def unique(arr):
    """Function for removing duplicated errors"""

    unique_arr = []
    for x in arr:
        if x not in unique_arr:
            unique_arr.append(x)
    return unique_arr

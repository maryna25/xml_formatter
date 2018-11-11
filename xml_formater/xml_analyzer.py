def analyze(path):
    file = open(path)
    line = file.read()

    tags = []  # stack to check if all tags are closed
    all_tags = []  # array with all tags
    errors = []  # array with all errors
    index = 1  # line number
    tag_name = ''  # tag name
    tag_type = 'opening'  # opening closing opening-closing
    quote_char = '"'  # opening quote for attribute value
    attr_name = ''  # attribute name
    xml_tag = False  # True if tag is <?xml ... ?>

    state = ''  # start_name name after_name closing_expected text attr_name quote_expected attr_value whitespace_expected

    for ch in line:
        # print(state, ch)
        if ch == "\n":
            index += 1
        if state == '':
            if ch == ' ' or ch == "\t" or ch == "\n":
                continue
            elif ch == '<':
                state = 'start_name'
                tag_type = 'opening'
            else:
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
                    state = 'closing_expected'
                else:
                    errors.append({index: 'Invalid tag name'})
            elif ch == ' ' or ch == "\t" or ch == "\n":
                state = 'after_name'
                if tag_type == 'opening':
                    if tag_name != '?xml':
                        tags.append(tag_name)
                    all_tags.append(tag_name)
                elif tag_type == 'closing':
                    if tags[-1] == tag_name:
                        tags.pop()
                    else:
                        errors.append({index: 'Unmatched closing tag'})
            elif ch == '>':
                state = 'text'
                if tag_type == 'opening':
                    if tag_name != '?xml':
                        tags.append(tag_name)
                    all_tags.append(tag_name)
                elif tag_type == 'closing':
                    if tags[-1] == tag_name:
                        tags.pop()
                    else:
                        errors.append({index: 'Unmatched closing tag'})
            else:
                errors.append({index: 'Invalid tag name'})
        elif state == 'after_name':
            if ch == ' ' or ch == "\t" or ch == "\n":
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
                state = 'start_name'
                tag_type = 'opening'
        elif state == 'attr_name':
            if ch.isalpha() or ch.isdigit() or ch == '.' or ch == '-' or ch == '_' or ch == ' ' or ch == "\t" or ch == "\n":
                attr_name += ch
            elif ch == '=':
                if attr_name[0:4] == 'xml:':
                    errors.pop()
                if attr_name == 'xml':
                    errors.append({index: 'xml cannot be attribute name'})
                attr_name = ''
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
                errors.append({index: 'Quote is expected'})
        elif state == 'attr_value':
            if ch == quote_char:
                state = 'whitespace_expected'
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
                    state = 'after_name'

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
                state = 'after_name'
            elif xml_tag and ch == '?':
                state = 'closing_expected'
            else:
                errors.append({index: 'Invalid tag'})

    if state != 'text':
        errors.append({index: 'XML is not valid'})
    if len(tags) > 0:
        errors.append({index: 'Some tags are not closed®'})

    # print(tags)
    # print(errors)
    # print(all_tags)
    # print(state)

    return errors


# analyze('text1.xml')


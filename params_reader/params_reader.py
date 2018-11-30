def read_params_from_input():
    params = {}
    print("Enter 1 if you want to use tab as indent char (default False)")
    params['use_tab'] = True if input() == 1 else False
    print("Enter tab size (default 4)")
    params['tab_size'] = input()
    print("Enter number of indent chars (default 4)")
    params['indent'] = input()
    print("Enter 1 to keep indents on empty line (default False)")
    params['keep_indents_on_empty_line'] = True if input() == 1 else False
    print("Enter 1 to keep line breaks (default True)")
    params['keep_line_breaks'] = True if input() == 1 else False
    print("Enter 1 to keep line breaks in text (default True)")
    params['keep_line_breaks_in_text'] = True if input() == 1 else False
    print("Enter number of blank lines to keep (default 2)")
    params['keep_blank_lines'] = input()
    print("Enter 0 if you to not wrap attrs, 1 - wrap if long, 2 - chomp down if long, 3 - wrap always (default 1)")
    params['wrap_attrs'] = input()
    print("Enter 1 if you want to wrap text (default True)")
    params['wrap_text'] = True if input() == 1 else False
    print("Enter 1 if you want to align attrs (default True)")
    params['align_attrs'] = True if input() == 1 else False
    print("Enter 1 if you want to keep whitespaces (default False)")
    params['keep_white_spaces'] = True if input() == 1 else False
    print("Enter 1 if you want to have space around equal (default False)")
    params['space_around_equal'] = True if input() == 1 else False
    print("Enter 1 if you want to have space space after tag name (default False)")
    params['space_after_tag_name'] = True if input() == 1 else False
    print("Enter 1 if you want to have space in empty tag (default False)")
    params['space_in_empty_tag'] = True if input() == 1 else False

    print("Enter file name to save")
    name = input()

    f = open(name, "w")
    f.write("\n".join(str(x) + '-' + str(params[x]) for x in params.keys()))
    f.write("\n")

    return params


def read_params_from_file(name):
    params = {}
    f = open(name, "r")
    lines = f.readlines()
    for line in lines:
        line_arr = line[:-1].split('-')
        value = line_arr[1]
        if value == 'True':
            value = True
        elif value == 'False':
            value = False
        elif value.isdigit():
            value = int(value)
        params[line_arr[0]] = value

    return params

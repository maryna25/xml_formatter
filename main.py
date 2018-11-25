import xml_formater

print("Hello!")
print("Enter 1 to only analyze xml")
print("Enter 2 to format xml with default configs")
print("Enter 3 to format xml with custom configs")

answer = input()

params = {}

if answer == 3:
    print("Enter 1 if you want to use tab as indent char (default False)")
    params['use_tab'] = True if input() == 1 else False
    print("Enter number of indent chars (default 4)")
    params['indent'] = input()
    print("Enter 1 to keep line breaks (default True)")
    params['keep_line_breaks'] = True if input() == 1 else False
    print("Enter number of blank lines to keep (default 2)")
    params['keep_blank_lines'] = input()
    print("Enter 1 if you want to wrap text (default True)")
    params['wrap_text'] = True if input() == 1 else False

errors, info = xml_formater.analyze('import.xml')
print(errors)

if answer > 1:
    f = open("result.txt", "w")
    f.write(xml_formater.format(info, params))

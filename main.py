import xml_formater
import params_reader


params_reader.read_params_from_file("kek.txt")

print("Hello!")
print("Enter 1 to only analyze xml")
print("Enter 2 to format xml with default configs")
print("Enter 3 to format xml with custom configs")
print("Enter 4 to format xml with custom configs from file")

answer = input()

params = {}

if answer == 3:
    params = params_reader.read_params_from_input()

if answer == 4:
    print("Enter file name")
    name = input()
    params = params_reader.read_params_from_file(name)

errors, info = xml_formater.analyze('import.xml')
print(errors)

if answer > 1:
    f = open("result.txt", "w")
    f.write(xml_formater.format(info, params))

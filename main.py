import xml_formater
import params_reader
import os.path

print("Hello! Check readme to find test instructions")
print("Enter file name")
file_name = input()
while not os.path.exists(file_name):
    print("Cannot find this file. Enter file name again")
    file_name = input()
print("Enter 1 to only analyze xml")
print("Enter 2 to format xml with default configs")
print("Enter 3 to format xml with custom configs")
print("Enter 4 to format xml with custom configs from file")

answer = input()

params = {}

if int(answer) == 3:
    params = params_reader.read_params_from_input()

if int(answer) == 4:
    print("Enter file name")
    name = input()
    params = params_reader.read_params_from_file(name)

errors, info = xml_formater.analyze(file_name)
print(errors)

if int(answer) > 1:
    f = open(file_name, "w")
    f.write(xml_formater.format(info, params))

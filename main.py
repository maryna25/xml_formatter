import xml_formater

errors, info = xml_formater.analyze('import.xml')

print(errors)

f = open("result.txt", "w")
f.write(xml_formater.format(info))
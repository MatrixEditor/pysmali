from smali import SmaliReader, SmaliWriter

reader = SmaliReader(comments=False)
writer = SmaliWriter(reader)

with open('example.smali', 'r', encoding='utf-8') as fp:
    source = fp.read()

reader.visit(source, writer)
print(writer.code)

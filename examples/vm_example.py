from smali.bridge import SmaliVM, SmaliObject

vm = SmaliVM()
with open('example.smali', 'r', encoding='utf-8') as fp:
    smali_class = vm.classloader.load_class(fp, init=False)

smali_class.clinit()

instance = SmaliObject(smali_class)
instance.init()

toString = instance.smali_class.method("toString")
value = toString(instance)

print(value)

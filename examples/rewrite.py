from typing import Optional
from smali import SmaliReader, SmaliWriter, MethodWriter


class CustomInstructionsWriter(MethodWriter):
    def __init__(self, delegate=None, indent=0) -> None:
        super().__init__(delegate, indent)

    # if you know the structure, it will be easy to install
    # the right hook
    def visit_registers(self, registers: int) -> None:
        super().visit_registers(registers)
        # add custom instruction
        self.visit_locals(1000)


class CustomWriter(SmaliWriter):
    def visit_method(
        self, name: str, access_flags: int, parameters: list, return_type: str
    ) -> Optional[MethodWriter]:
        if name == "main":
            return CustomInstructionsWriter()



reader = SmaliReader(comments=False)
writer = SmaliWriter(reader, delegate=CustomWriter())

with open("rewrite.smali", "r", encoding="utf-8") as fp:
    source = fp.read()

reader.visit(source, writer)
print(writer.code)
from dataclasses import dataclass
from typing import List, Dict

from immolate.cpu import Cpu
from immolate.instructions import Instruction, _parse_register


@dataclass
class PrintRegister(Instruction):
    register: int  # 2

    def execute(self, cpu: Cpu):
        cpu.do_output(cpu.registers[self.register])

    @staticmethod
    def decode(b: bytes):
        register = b[0]
        return PrintRegister(register)

    def __bytes__(self) -> bytes:
        return bytes([self.register, 0])

    @staticmethod
    def decode_assembly(tokens: List[str], labels: Dict[str, int]):
        register = _parse_register(tokens[1])
        return PrintRegister(register)

    def __str__(self):
        return f"{self.assembly_name()} r{self.register}"

    @staticmethod
    def assembly_name() -> str:
        return "PRINT"

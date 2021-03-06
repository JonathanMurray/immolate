from dataclasses import dataclass
from typing import List, Dict

from immolate.cpu import Cpu
from immolate.instructions import Instruction, _parse_register


@dataclass
class Push(Instruction):
    value: int  # 8

    def __post_init__(self):
        Cpu.assert_fits_in_word(self.value)

    def execute(self, cpu: Cpu):
        cpu.stack.append(self.value)

    @staticmethod
    def decode(b: bytes):
        value = b[0]
        return Push(value)

    def __bytes__(self) -> bytes:
        return bytes([self.value, 0])

    @staticmethod
    def decode_assembly(tokens: List[str], labels: Dict[str, int]):
        value = int(tokens[1])
        return Push(value)

    def __str__(self):
        return f"{self.assembly_name()} {self.value}"

    @staticmethod
    def assembly_name() -> str:
        return "PUSH"


@dataclass
class Pop(Instruction):
    register: int

    def execute(self, cpu: Cpu):
        cpu.registers[self.register] = cpu.stack.pop()

    @staticmethod
    def decode(b: bytes):
        register = b[0]
        return Pop(register)

    def __bytes__(self) -> bytes:
        return bytes([self.register, 0])

    @staticmethod
    def decode_assembly(tokens: List[str], labels: Dict[str, int]):
        register = _parse_register(tokens[1])
        return Pop(register)

    def __str__(self):
        return f"{self.assembly_name()} r{self.register}"

    @staticmethod
    def assembly_name() -> str:
        return "POP"

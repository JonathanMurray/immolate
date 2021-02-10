from dataclasses import dataclass
from typing import List, Dict

from immolate.cpu import Cpu
from immolate.instructions import Instruction, _assert_left_arrow, _parse_register


@dataclass
class Put(Instruction):
    value: int  # 8
    register: int  # 2

    def __post_init__(self):
        Cpu.assert_fits_in_word(self.value)

    def execute(self, cpu: Cpu):
        cpu.registers[self.register] = self.value

    @staticmethod
    def decode(b: bytes):
        value = b[0]
        register = b[1]
        return Put(value, register)

    def __bytes__(self) -> bytes:
        return bytes([self.value, self.register])

    @staticmethod
    def decode_assembly(tokens: List[str], labels: Dict[str, int]):
        register = _parse_register(tokens[1])
        _assert_left_arrow(tokens[2])
        value = int(tokens[3])
        return Put(value, register)

    def __str__(self):
        return f"{self.assembly_name()} r{self.register} <- {self.value}"

    @staticmethod
    def assembly_name() -> str:
        return "PUT"

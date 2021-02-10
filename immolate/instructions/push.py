from dataclasses import dataclass
from typing import List, Dict

from immolate.cpu import Cpu
from immolate.instructions import Instruction


@dataclass
class Push(Instruction):
    value: int  # 8

    def __post_init__(self):
        Cpu.assert_fits_in_register(self.value)

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

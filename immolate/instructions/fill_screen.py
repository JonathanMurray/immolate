from dataclasses import dataclass
from typing import List, Dict

from immolate.cpu import Cpu
from immolate.instructions import Instruction, _parse_register


@dataclass
class FillScreen(Instruction):
    color_register: int

    def execute(self, cpu: Cpu):
        cpu.fill_screen(cpu.registers[self.color_register])

    @staticmethod
    def decode(b: bytes):
        color_register = int(b[0])
        return FillScreen(color_register)

    def __bytes__(self) -> bytes:
        return bytes([self.color_register, 0])

    @staticmethod
    def decode_assembly(tokens: List[str], labels: Dict[str, int]):
        color_register = _parse_register(tokens[1])
        return FillScreen(color_register)

    def __str__(self):
        return f"{self.assembly_name()} r{self.color_register}"

    @staticmethod
    def assembly_name() -> str:
        return "FILL_SCREEN"

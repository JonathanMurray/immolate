from dataclasses import dataclass
from typing import List, Dict

from immolate.cpu import Cpu
from immolate.instructions import Instruction


@dataclass
class Breakpoint(Instruction):

    def execute(self, cpu: Cpu):
        cpu.halted = True

    @staticmethod
    def decode(b: bytes):
        return Breakpoint()

    def __bytes__(self) -> bytes:
        return bytes(2)

    @staticmethod
    def decode_assembly(tokens: List[str], labels: Dict[str, int]):
        return Breakpoint()

    def __str__(self):
        return f"{self.assembly_name()}"

    @staticmethod
    def assembly_name() -> str:
        return "BREAKPOINT"

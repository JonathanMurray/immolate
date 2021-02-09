from dataclasses import dataclass
from typing import List, Dict

from immolate.cpu import Cpu
from immolate.instructions import Instruction


@dataclass
class Exit(Instruction):
    exit_code: int  # 8

    def execute(self, cpu: Cpu):
        cpu.exit_code = self.exit_code
        cpu.has_exited = True

    @staticmethod
    def decode(b: bytes):
        exit_code = b[0]
        return Exit(exit_code)

    def __bytes__(self) -> bytes:
        return bytes([self.exit_code, 0])

    @staticmethod
    def decode_assembly(tokens: List[str], labels: Dict[str, int]):
        exit_code = int(tokens[1])
        return Exit(exit_code)

    def __str__(self):
        return f"{self.assembly_name()} {self.exit_code}"

    @staticmethod
    def assembly_name() -> str:
        return "EXIT"

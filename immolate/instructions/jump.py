from dataclasses import dataclass
from typing import List, Dict

from immolate.cpu import Cpu
from immolate.instructions import Instruction, _parse_jump_destination


@dataclass
class Jump(Instruction):
    instruction_index: int  # 8

    def execute(self, cpu: Cpu):
        cpu.instruction_pointer = self.instruction_index

    @staticmethod
    def decode(b: bytes):
        instruction_index = b[0]
        return Jump(instruction_index)

    def __bytes__(self) -> bytes:
        return bytes([self.instruction_index, 0])

    @staticmethod
    def decode_assembly(tokens: List[str], labels: Dict[str, int]):
        instruction_index = _parse_jump_destination(tokens[1], labels)
        return Jump(instruction_index)

    def __str__(self):
        return f"{self.assembly_name()} {self.instruction_index}"

    @staticmethod
    def assembly_name() -> str:
        return "JUMP"

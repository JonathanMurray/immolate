from dataclasses import dataclass
from typing import List, Dict

from immolate.cpu import Cpu
from immolate.instructions import Instruction, _parse_jump_destination


@dataclass
class CallSubroutine(Instruction):
    instruction_index: int  # 8

    def execute(self, cpu: Cpu):
        cpu.stack.append(cpu.instruction_pointer)
        cpu.instruction_pointer = self.instruction_index

    @staticmethod
    def decode(b: bytes):
        instruction_index = b[0]
        return CallSubroutine(instruction_index)

    def __bytes__(self) -> bytes:
        return bytes([self.instruction_index, 0])

    @staticmethod
    def decode_assembly(tokens: List[str], labels: Dict[str, int]):
        instruction_index = _parse_jump_destination(tokens[1], labels)
        return CallSubroutine(instruction_index)

    def __str__(self):
        return f"{self.assembly_name()} {self.instruction_index}"

    @staticmethod
    def assembly_name() -> str:
        return "CALL_SUBROUTINE"


@dataclass
class Return(Instruction):

    def execute(self, cpu: Cpu):
        return_address = cpu.stack.pop()
        cpu.instruction_pointer = return_address

    @staticmethod
    def decode(b: bytes):
        return Return()

    def __bytes__(self) -> bytes:
        return bytes([0, 0])

    @staticmethod
    def decode_assembly(tokens: List[str], labels: Dict[str, int]):
        return Return()

    def __str__(self):
        return f"{self.assembly_name()}"

    @staticmethod
    def assembly_name() -> str:
        return "RETURN"

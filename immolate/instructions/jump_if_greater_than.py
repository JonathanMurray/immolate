from dataclasses import dataclass
from typing import List, Dict

from immolate.cpu import Cpu
from immolate.instructions import Instruction, _assert_left_arrow, _parse_register, _parse_jump_destination


@dataclass
class JumpIfGreaterThan(Instruction):
    register_a: int  # 2
    register_b: int  # 2
    instruction_index: int  # 8

    def execute(self, cpu: Cpu):
        if cpu.registers[self.register_a] > cpu.registers[self.register_b]:
            cpu.instruction_pointer = self.instruction_index

    @staticmethod
    def decode(b: bytes):
        register_a = (b[0] & 0b00001100) >> 2
        register_b = b[0] & 0b00000011
        instruction_index = b[1]
        return JumpIfGreaterThan(register_a, register_b, instruction_index)

    def __bytes__(self) -> bytes:
        return bytes([(self.register_a << 2) + self.register_b, self.instruction_index])

    @staticmethod
    def decode_assembly(tokens: List[str], labels: Dict[str, int]):
        instruction_index = _parse_jump_destination(tokens[1], labels)
        _assert_left_arrow(tokens[2])
        register_a = _parse_register(tokens[3])
        register_b = _parse_register(tokens[4])
        return JumpIfGreaterThan(register_a, register_b, instruction_index)

    def __str__(self):
        return f"{self.assembly_name()} {self.instruction_index} <- r{self.register_a} r{self.register_b}"

    @staticmethod
    def assembly_name() -> str:
        return "JUMP_GT"

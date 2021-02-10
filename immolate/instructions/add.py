from dataclasses import dataclass
from typing import List, Dict

from immolate.cpu import Cpu
from immolate.instructions import Instruction, _assert_arrow, _parse_register


@dataclass
class Add(Instruction):
    register_a: int  # 2
    register_b: int  # 2
    destination_register: int  # 2

    def execute(self, cpu: Cpu):
        cpu.add(cpu.registers[self.register_a], cpu.registers[self.register_b], self.destination_register)

    @staticmethod
    def decode(b: bytes):
        register_a = (b[0] & 0b00110000) >> 4
        register_b = (b[0] & 0b00001100) >> 2
        destination_register = b[0] & 0b00000011
        return Add(register_a, register_b, destination_register)

    def __bytes__(self) -> bytes:
        return bytes([(self.register_a << 4) + (self.register_b << 2) + self.destination_register, 0])

    @staticmethod
    def decode_assembly(tokens: List[str], labels: Dict[str, int]):
        destination_register = _parse_register(tokens[1])
        _assert_arrow(tokens[2])
        register_a = _parse_register(tokens[3])
        register_b = _parse_register(tokens[4])
        return Add(register_a, register_b, destination_register)

    def __str__(self):
        return f"{self.assembly_name()} r{self.destination_register} <- r{self.register_a} r{self.register_b}"

    @staticmethod
    def assembly_name() -> str:
        return "ADD"

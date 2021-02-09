from dataclasses import dataclass
from typing import List, Dict

from immolate.cpu import Cpu
from immolate.instructions import Instruction, _assert_arrow, _parse_register


@dataclass
class AddRegisterAndNumber(Instruction):
    number: int  # 8
    source_register: int  # 2
    destination_register: int  # 2

    def execute(self, cpu: Cpu):
        cpu.registers[self.destination_register] = cpu.registers[self.source_register] + self.number

    @staticmethod
    def decode(b: bytes):
        number = b[0]
        source_register = (b[1] & 0b00001100) >> 2
        destination_register = b[1] & 0b00000011
        return AddRegisterAndNumber(number, source_register, destination_register)

    def __bytes__(self) -> bytes:
        return bytes([self.number, (self.source_register << 2) + self.destination_register])

    @staticmethod
    def decode_assembly(tokens: List[str], labels: Dict[str, int]):
        destination_register = _parse_register(tokens[1])
        _assert_arrow(tokens[2])
        source_register = _parse_register(tokens[3])
        number = int(tokens[4])

        return AddRegisterAndNumber(number, source_register, destination_register)

    def __str__(self):
        return f"{self.assembly_name()} r{self.destination_register} <- r{self.source_register} {self.number}"

    @staticmethod
    def assembly_name() -> str:
        return "ADD_NUM"

from dataclasses import dataclass
from typing import List, Dict

from immolate.cpu import Cpu
from immolate.instructions import Instruction, _assert_right_arrow, _parse_memory_address, _parse_register, \
    _assert_left_arrow


@dataclass
class Store(Instruction):
    value: int  # 8
    address: int  # 8

    def __post_init__(self):
        Cpu.assert_fits_in_word(self.value)
        Cpu.assert_fits_in_word(self.address)

    def execute(self, cpu: Cpu):
        cpu.memory[self.address] = self.value

    @staticmethod
    def decode(b: bytes):
        value = b[0]
        address = b[1]
        return Store(value, address)

    def __bytes__(self) -> bytes:
        return bytes([self.value, self.address])

    @staticmethod
    def decode_assembly(tokens: List[str], labels: Dict[str, int]):
        value = int(tokens[1])
        _assert_right_arrow(tokens[2])
        address = _parse_memory_address(tokens[3])
        return Store(value, address)

    def __str__(self):
        return f"{self.assembly_name()} {self.value} -> [{self.address}]"

    @staticmethod
    def assembly_name() -> str:
        return "STORE"


@dataclass
class Load(Instruction):
    destination_register: int
    address: int

    def __post_init__(self):
        Cpu.assert_fits_in_word(self.address)

    def execute(self, cpu: Cpu):
        cpu.registers[self.destination_register] = cpu.memory[self.address]

    @staticmethod
    def decode(b: bytes):
        register = b[0]
        address = b[1]
        return Load(register, address)

    def __bytes__(self) -> bytes:
        return bytes([self.destination_register, self.address])

    @staticmethod
    def decode_assembly(tokens: List[str], labels: Dict[str, int]):
        register = _parse_register(tokens[1])
        _assert_left_arrow(tokens[2])
        address = _parse_memory_address(tokens[3])
        return Load(register, address)

    def __str__(self):
        return f"{self.assembly_name()} r{self.destination_register} <- [{self.address}]"

    @staticmethod
    def assembly_name() -> str:
        return "LOAD"

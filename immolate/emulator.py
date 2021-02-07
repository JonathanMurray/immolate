from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import List


class Instruction(metaclass=ABCMeta):
    @abstractmethod
    def execute(self, cpu):
        pass

    @staticmethod
    @abstractmethod
    def decode(b: bytes):
        pass

    @abstractmethod
    def __bytes__(self) -> bytes:
        pass

    @staticmethod
    @abstractmethod
    def decode_assembly(tokens: List[str]):
        pass

    @staticmethod
    @abstractmethod
    def assembly_name() -> str:
        pass


class Cpu:
    def __init__(self, program: List[Instruction], debug: bool = False):
        self.registers = [0, 0, 0, 0]
        self._program = program
        self.instruction_pointer = 0
        self.has_exited = False
        self.exit_code = None
        self.output = []
        self._debug = debug

    def run_one_cycle(self):
        if self.instruction_pointer >= len(self._program):
            raise Exception("CPU crashed - trying to read past the last instruction!")
        instruction = self._program[self.instruction_pointer]
        self.instruction_pointer += 1
        if self._debug:
            print(f"Executing {instruction}")
        instruction.execute(self)

    def run_until_exit(self):
        while not self.has_exited:
            self.run_one_cycle()

    def __str__(self):
        return f"Reg: {self.registers}, Instruction pointer: {self.instruction_pointer}"


@dataclass
class Put(Instruction):
    value: int  # 8
    register: int  # 2

    def execute(self, cpu: Cpu):
        cpu.registers[self.register] = self.value

    @staticmethod
    def decode(b: bytes):
        value = b[0]
        register = b[1]
        return Put(value, register)

    def __bytes__(self) -> bytes:
        return bytes([self.value, self.register])

    @staticmethod
    def decode_assembly(tokens: List[str]):
        register = _parse_register(tokens[1])
        _assert_arrow(tokens[2])
        value = int(tokens[3])
        return Put(value, register)

    def __str__(self):
        return f"{self.assembly_name()} r{self.register} <- {self.value}"

    @staticmethod
    def assembly_name() -> str:
        return "PUT"


@dataclass
class Add(Instruction):
    register_a: int  # 2
    register_b: int  # 2
    destination_register: int  # 2

    def execute(self, cpu: Cpu):
        cpu.registers[self.destination_register] = cpu.registers[self.register_a] + cpu.registers[self.register_b]

    @staticmethod
    def decode(b: bytes):
        register_a = (b[0] & 0b00110000) >> 4
        register_b = (b[0] & 0b00001100) >> 2
        destination_register = b[0] & 0b00000011
        return Add(register_a, register_b, destination_register)

    def __bytes__(self) -> bytes:
        return bytes([(self.register_a << 4) + (self.register_b << 2) + self.destination_register, 0])

    @staticmethod
    def decode_assembly(tokens: List[str]):
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
    def decode_assembly(tokens: List[str]):
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
    def decode_assembly(tokens: List[str]):
        instruction_index = int(tokens[1])
        return Jump(instruction_index)

    def __str__(self):
        return f"{self.assembly_name()} {self.instruction_index}"

    @staticmethod
    def assembly_name() -> str:
        return "JUMP"


@dataclass
class JumpIfEqual(Instruction):
    register_a: int  # 2
    register_b: int  # 2
    instruction_index: int  # 8

    def execute(self, cpu: Cpu):
        if cpu.registers[self.register_a] == cpu.registers[self.register_b]:
            cpu.instruction_pointer = self.instruction_index

    @staticmethod
    def decode(b: bytes):
        register_a = (b[0] & 0b00001100) >> 2
        register_b = b[0] & 0b00000011
        instruction_index = b[1]
        return JumpIfEqual(register_a, register_b, instruction_index)

    def __bytes__(self) -> bytes:
        return bytes([(self.register_a << 2) + self.register_b, self.instruction_index])

    @staticmethod
    def decode_assembly(tokens: List[str]):
        instruction_index = int(tokens[1])
        _assert_arrow(tokens[2])
        register_a = _parse_register(tokens[3])
        register_b = _parse_register(tokens[4])
        return JumpIfEqual(register_a, register_b, instruction_index)

    def __str__(self):
        return f"{self.assembly_name()} {self.instruction_index} <- r{self.register_a} r{self.register_b}"

    @staticmethod
    def assembly_name() -> str:
        return "JUMP_EQ"


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
    def decode_assembly(tokens: List[str]):
        exit_code = int(tokens[1])
        return Exit(exit_code)

    def __str__(self):
        return f"{self.assembly_name()} {self.exit_code}"

    @staticmethod
    def assembly_name() -> str:
        return "EXIT"


@dataclass
class PrintRegister(Instruction):
    register: int  # 2

    def execute(self, cpu: Cpu):
        cpu.output.append(str(cpu.registers[self.register]))

    @staticmethod
    def decode(b: bytes):
        register = b[0]
        return PrintRegister(register)

    def __bytes__(self) -> bytes:
        return bytes([self.register, 0])

    @staticmethod
    def decode_assembly(tokens: List[str]):
        register = _parse_register(tokens[1])
        return PrintRegister(register)

    def __str__(self):
        return f"{self.assembly_name()} r{self.register}"

    @staticmethod
    def assembly_name() -> str:
        return "PRINT"


def _assert_arrow(token: str):
    if token != "<-":
        raise ValueError(f"Expected '<-' but got '{token}'")


def _parse_register(token: str) -> int:
    if not token.startswith("r"):
        raise ValueError(f"Expected register token but got '{token}'")
    return int(token[1:])

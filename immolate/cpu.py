from time import sleep
from typing import List

from immolate.instructions import Instruction
from immolate.screen import Screen, FakeScreen


class Cpu:
    REGISTER_SIZE = 256  # 8-bit

    def __init__(self, program: List[Instruction], args: List[int] = None, debug: bool = False,
        allow_sleeps: bool = False, screen: Screen = None):
        if len(program) >= Cpu.REGISTER_SIZE:
            raise ValueError(f"Program too large for address space. Len={program}")
        args = args or []
        if len(args) > 4:
            raise ValueError(f"Max 4 args are allowed. Got {len(args)}: {args}")

        self.registers = [0, 0, 0, 0]
        for i in range(len(args)):
            self.registers[i] = args[i]
        self.carry_flag = None
        self._program = program
        self.output = []
        self.instruction_pointer = 0
        self.has_exited = False
        self.exit_code = None
        self._debug = debug
        self._allow_sleeps = allow_sleeps
        self._screen = screen or FakeScreen()
        self.halted = False
        self.stack = []

    def add(self, a: int, b: int, destination_register: int):
        result = a + b
        self.registers[destination_register] = result % Cpu.REGISTER_SIZE
        self.carry_flag = result >= Cpu.REGISTER_SIZE

    def do_output(self, output: int):
        print(str(output))
        self.output.append(str(output))

    def run_until_exit_or_halt(self):
        if self.has_exited:
            raise Exception("CPU has exited!")
        if self.halted:
            raise Exception("CPU has halted!")
        while not self.has_exited and not self.halted:
            self.run_one_cycle()

    def run_one_cycle(self):
        if self.instruction_pointer >= len(self._program):
            raise Exception("Can't read past the last instruction!")
        instruction = self._program[self.instruction_pointer]
        self.instruction_pointer += 1
        if self._debug:
            print(f"Executing {instruction}")
        instruction.execute(self)

    def __str__(self):
        return f"Reg: {self.registers}, Instruction pointer: {self.instruction_pointer}"

    def sleep(self, millis: int):
        if self._allow_sleeps:
            sleep(millis / 1000.0)

    def activate_screen(self):
        self._screen.activate()
        self._screen.run_one_frame()

    def refresh_screen(self):
        self._screen.run_one_frame()

    def fill_screen(self, color: int):
        self._screen.color = color

    def dump(self) -> str:
        return (
            f"+----------------------+\n"
            f"|  CPU                 |\n"
            f"|                      |\n"
            f"|  registers:          |\n"
            f"| +---------------+    |\n"
            f"| |{self.registers[0]: >3}"
            f"|{self.registers[1]: >3}"
            f"|{self.registers[2]: >3}"
            f"|{self.registers[3]: >3}|    |\n"
            f"| +---------------+    |\n"
            f"|                      |\n"
            f"|  instr. ptr: {self.instruction_pointer: > 3}     |\n"
            f"|                      |\n"
            f"|  next instruction:   |\n"
            f"|  {str(self._program[self.instruction_pointer]).ljust(20)}|\n"
            f"+----------------------+"
        )

    @staticmethod
    def assert_fits_in_register(value: int):
        if value >= Cpu.REGISTER_SIZE:
            raise ValueError(f"Expected value that fits in register, but got: {value}")

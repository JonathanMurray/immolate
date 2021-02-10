from immolate.cpu import Cpu
from immolate.example_programs import FIBONACCI, PRINT_1337, ADD_TWO_ARGS, GRAPHICS, BREAKPOINT
from immolate.screen import FakeScreen


def test_fibonacci():
    cpu = Cpu(FIBONACCI)
    cpu.run_until_exit_or_halt()
    # Fibonacci sequence loops around at 255
    assert cpu.output == ["0", "1", "1", "2", "3", "5", "8", "13", "21", "34", "55", "89", "144", "233", "121", "98"]


def test_1337():
    cpu = Cpu(PRINT_1337)
    cpu.run_until_exit_or_halt()
    assert cpu.output == ["1", "3", "3", "7"]


def test_add_two_args():
    cpu = Cpu(ADD_TWO_ARGS, args=[38, 4])
    cpu.run_until_exit_or_halt()
    assert cpu.output == ["42"]


def test_graphics():
    screen = FakeScreen()
    cpu = Cpu(GRAPHICS, screen=screen)
    cpu.run_until_exit_or_halt()
    assert cpu.output == []
    assert screen.color == 254


def test_breakpoint():
    cpu = Cpu(BREAKPOINT)
    cpu.run_until_exit_or_halt()
    assert cpu.output == ["1"]
    assert cpu.halted
    cpu.halted = False
    cpu.run_until_exit_or_halt()
    assert cpu.output == ["1", "2"]

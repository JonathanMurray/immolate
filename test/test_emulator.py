from immolate.emulator import Cpu
from immolate.example_programs import FIBONACCI, PRINT_1337, ADD_TWO_ARGS, GRAPHICS
from immolate.screen import FakeScreen


def test_fibonacci():
    cpu = Cpu(FIBONACCI)
    cpu.run_until_exit()
    assert cpu.output == ["0", "1", "1", "2", "3", "5", "8", "13", "21", "34", "55", "89"]


def test_1337():
    cpu = Cpu(PRINT_1337)
    cpu.run_until_exit()
    assert cpu.output == ["1", "3", "3", "7"]


def test_add_two_args():
    cpu = Cpu(ADD_TWO_ARGS, args=[38, 4])
    cpu.run_until_exit()
    assert cpu.output == ["42"]


def test_graphics():
    screen = FakeScreen()
    cpu = Cpu(GRAPHICS, screen=screen)
    cpu.run_until_exit()
    assert cpu.output == []
    assert screen.color == 254

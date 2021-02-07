from immolate.emulator import Cpu
from immolate.example_programs import FIBONACCI, PRINT_1337


def test_fibonacci():
    cpu = Cpu(FIBONACCI)
    cpu.run_until_exit()
    assert cpu.output == ["0", "1", "1", "2", "3", "5", "8", "13", "21", "34", "55", "89"]


def test_1337():
    cpu = Cpu(PRINT_1337)
    cpu.run_until_exit()
    assert cpu.output == ["1", "3", "3", "7"]

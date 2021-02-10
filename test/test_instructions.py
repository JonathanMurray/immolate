from pytest import fail

from immolate.cpu import Cpu
from immolate.instructions.add import Add
from immolate.instructions.add_register_and_number import AddRegisterAndNumber
from immolate.instructions.put import Put


def test_add():
    cpu = Cpu([])
    cpu.registers[0] = 10
    cpu.registers[1] = 20

    Add(0, 1, 2).execute(cpu)

    assert cpu.registers[2] == 30


def test_add_carry():
    cpu = Cpu([])
    cpu.registers[0] = 250
    cpu.registers[1] = 6

    Add(0, 1, 2).execute(cpu)

    assert cpu.registers[2] == 0
    assert cpu.carry_flag


def test_add_register_and_number_carry():
    cpu = Cpu([])
    cpu.registers[0] = 250

    AddRegisterAndNumber(50, 0, 1).execute(cpu)

    assert cpu.registers[1] == 44
    assert cpu.carry_flag


def test_put():
    try:
        Put(256, 0)
        fail("Should not allow putting a value that's larger than 255!")
    except ValueError:
        pass

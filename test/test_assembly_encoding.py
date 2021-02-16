from immolate.encoding.assembly import load_from_file, parse_assembly_line, parse_instruction_tokens
from immolate.example_programs import FIBONACCI
from immolate.instructions.activate_screen import ActivateScreen
from immolate.instructions.add import Add
from immolate.instructions.add_register_and_number import AddRegisterAndNumber
from immolate.instructions.breakpoint import Breakpoint
from immolate.instructions.classes import INSTRUCTION_CLASSES
from immolate.instructions.exit import Exit
from immolate.instructions.jump import Jump
from immolate.instructions.jump_if_equal import JumpIfEqual
from immolate.instructions.memory import Store, Load
from immolate.instructions.print_register import PrintRegister
from immolate.instructions.put import Put
from immolate.instructions.refresh_screen import RefreshScreen
from immolate.instructions.sleep import Sleep
from immolate.instructions.stack import Push, Pop
from immolate.instructions.subroutine import CallSubroutine, Return

EXAMPLE_INSTRUCTIONS = [
    (["PUT", "r1", "<-", "42"], Put(42, 1)),
    (["ADD", "r3", "<-", "r1", "r2"], Add(1, 2, 3)),
    (["ADD_NUM", "r2", "<-", "r1", "42"], AddRegisterAndNumber(42, 1, 2)),
    (["JUMP", "42"], Jump(42)),
    (["JUMP_EQ", "42", "<-", "r1", "r2"], JumpIfEqual(1, 2, 42)),
    (["EXIT", "1"], Exit(1)),
    (["PRINT", "r1"], PrintRegister(1)),
    (["SLEEP", "1000"], Sleep(1000)),
    (["ACTIVATE_SCREEN"], ActivateScreen()),
    (["REFRESH_SCREEN"], RefreshScreen()),
    (["BREAKPOINT"], Breakpoint()),
    (["PUSH", "42"], Push(42)),
    (["POP", "r1"], Pop(1)),
    (["CALL_SUBROUTINE", "42"], CallSubroutine(42)),
    (["RETURN"], Return()),
    (["STORE", "r1", "->", "[123]"], Store(1, 123)),
    (["LOAD", "r1", "<-", "[123]"], Load(1, 123)),
]


def test_all_instructions_are_tested():
    for cls in INSTRUCTION_CLASSES:
        print(f"Asserting that instruction {cls} is tested.")
        assert any(type(instruction) == cls for (_, instruction) in EXAMPLE_INSTRUCTIONS)


def test_parse_instruction_tokens():
    for (tokens, instruction) in EXAMPLE_INSTRUCTIONS:
        assert parse_instruction_tokens(tokens, {}) == instruction
        assert str(instruction) == " ".join(tokens)


def test_parse_jump_instructions_with_labels():
    assert parse_instruction_tokens(["JUMP", "A"], {"A": 42, "B": 999}) == Jump(42)
    assert parse_instruction_tokens(["JUMP_EQ", "A", "<-", "r1", "r2"], {"A": 42, "B": 999}) == JumpIfEqual(1, 2, 42)


def test_fibonacci_program():
    sprite_paths, program = load_from_file("files/fibonacci_assembly.txt")
    assert sprite_paths == []
    assert program == FIBONACCI


def test_graphics_program():
    sprite_paths, program = load_from_file("files/graphics_assembly.txt")
    assert len(sprite_paths) == 2
    assert type(sprite_paths[0]) == bytes
    assert type(sprite_paths[1]) == bytes
    assert len(program) > 0


def test_parse_assembly_line():
    assert parse_assembly_line("  ADD    r3 <- r1  r2  # this is a comment", {}) == Add(1, 2, 3)

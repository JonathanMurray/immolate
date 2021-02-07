from immolate.assembler import parse_instruction_tokens, parse_assembly_line, load_program_from_assembly_file
from immolate.emulator import Put, PrintRegister, Exit, Add, AddRegisterAndNumber, Jump, JumpIfEqual, Sleep, \
    ActivateScreen, FillScreen, RefreshScreen, Instruction
from immolate.example_programs import FIBONACCI

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
    (["FILL_SCREEN", "r1"], FillScreen(1)),
    (["REFRESH_SCREEN"], RefreshScreen()),
]


def test_all_instructions_are_tested():
    for cls in Instruction.__subclasses__():
        print(f"Asserting that instruction {cls} is tested.")
        assert any(type(instruction) == cls for (_, instruction) in EXAMPLE_INSTRUCTIONS)


def test_parse_instruction_tokens():
    for (tokens, instruction) in EXAMPLE_INSTRUCTIONS:
        assert parse_instruction_tokens(tokens, {}) == instruction
        assert str(instruction) == " ".join(tokens)


def test_parse_jump_instructions_with_labels():
    assert parse_instruction_tokens(["JUMP", "A"], {"A": 42, "B": 999}) == Jump(42)
    assert parse_instruction_tokens(["JUMP_EQ", "A", "<-", "r1", "r2"], {"A": 42, "B": 999}) == JumpIfEqual(1, 2, 42)


def test_fibonacci_example():
    program = load_program_from_assembly_file("files/fibonacci_assembly.txt")
    assert program == FIBONACCI


def test_parse_assembly_line():
    assert parse_assembly_line("  ADD    r3 <- r1  r2  # this is a comment", {}) == Add(1, 2, 3)

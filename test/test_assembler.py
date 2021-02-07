from immolate.assembler import parse_instruction_tokens, parse_assembly_line, load_program_from_assembly_file
from immolate.emulator import Put, PrintRegister, Exit, Add, AddRegisterAndNumber, Jump, JumpIfEqual
from immolate.example_programs import FIBONACCI


def test_parse_instruction_tokens():
    assert parse_instruction_tokens(["PUT", "r1", "<-", "42"], {}) == Put(42, 1)
    assert parse_instruction_tokens(["ADD", "r3", "<-", "r1", "r2"], {}) == Add(1, 2, 3)
    assert parse_instruction_tokens(["ADD_NUM", "r2", "<-", "r1", "42"], {}) == AddRegisterAndNumber(42, 1, 2)
    assert parse_instruction_tokens(["JUMP", "42"], {}) == Jump(42)
    assert parse_instruction_tokens(["JUMP_EQ", "42", "<-", "r1", "r2"], {}) == JumpIfEqual(1, 2, 42)
    assert parse_instruction_tokens(["EXIT", "1"], {}) == Exit(1)
    assert parse_instruction_tokens(["PRINT", "r1"], {}) == PrintRegister(1)


def test_parse_jump_instructions_with_labels():
    assert parse_instruction_tokens(["JUMP", "A"], {"A": 42, "B": 999}) == Jump(42)
    assert parse_instruction_tokens(["JUMP_EQ", "A", "<-", "r1", "r2"], {"A": 42, "B": 999}) == JumpIfEqual(1, 2, 42)


def test_assembly_encoding_roundtrip():
    instructions = [
        Put(42, 1),
        Add(1, 2, 3),
        AddRegisterAndNumber(42, 1, 2),
        Jump(1),
        JumpIfEqual(1, 2, 42),
        Exit(42),
        PrintRegister(1),
    ]

    for instruction in instructions:
        print(f"\nTesting instruction: {instruction}")
        assembly = str(instruction)
        print(f"Encoded: {assembly}")
        decoded = parse_assembly_line(assembly, {})
        print(f"Decoded: {decoded}")
        assert instruction == decoded


def test_fibonacci_example():
    program = load_program_from_assembly_file("files/fibonacci_assembly.txt")
    assert program == FIBONACCI


def test_parse_assembly_line():
    assert parse_assembly_line("  ADD    r3 <- r1  r2  # this is a comment", {}) == Add(1, 2, 3)

import os
import tempfile

from immolate.emulator import Put, Add, AddRegisterAndNumber, Jump, JumpIfEqual, Exit, PrintRegister
from immolate.encoding import decode_instruction, encode_instruction, save_program_to_file, load_program_from_file
from immolate.example_programs import FIBONACCI, PRINT_1337


def test_instruction_encoding():
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
        encoded = encode_instruction(instruction)
        print(f"Encoded: {encoded}")
        decoded = decode_instruction(encoded)
        print(f"Decoded: {decoded}")
        assert instruction == decoded


def test_program_encoding():
    programs = [FIBONACCI, PRINT_1337]
    with tempfile.TemporaryDirectory() as tempdir:
        for i, program in enumerate(programs):
            print(f"Program: {program}")
            filepath = os.path.join(tempdir, f"test_program_{i}")
            save_program_to_file(program, filepath)
            print(f"Saved to {filepath}")
            loaded_program = load_program_from_file(filepath)
            print(f"Loaded program: {loaded_program}")
            assert program == loaded_program

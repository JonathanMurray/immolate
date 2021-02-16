import os
import tempfile

from immolate.encoding.binary import decode_instruction, encode_instruction, save_program_to_file, \
    load_program_from_file
from immolate.example_programs import EXAMPLE_PROGRAMS
from test.test_assembly_encoding import EXAMPLE_INSTRUCTIONS


def test_instruction_encoding():
    for (_, instruction) in EXAMPLE_INSTRUCTIONS:
        print(f"\nTesting instruction: {instruction}")
        encoded = encode_instruction(instruction)
        print(f"Encoded: {encoded}")
        decoded = decode_instruction(encoded)
        print(f"Decoded: {decoded}")
        assert instruction == decoded


def test_program_encoding():
    with tempfile.TemporaryDirectory() as tempdir:
        for i, (sprites, program) in enumerate(EXAMPLE_PROGRAMS.values()):
            print(f"Program: {program}")
            filepath = os.path.join(tempdir, f"test_program_{i}")
            save_program_to_file(program, sprites, filepath)
            print(f"Saved to {filepath}")
            loaded_program, loaded_sprites = load_program_from_file(filepath)
            print(f"Loaded program: {loaded_program}")
            assert program == loaded_program
            assert sprites == loaded_sprites

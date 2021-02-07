from typing import List

from immolate.emulator import Instruction
from immolate.encoding import INSTRUCTION_CLASSES


def load_program_from_assembly_file(filename: str) -> List[Instruction]:
    program = []
    print(f"Loading program from {filename}")
    with open(filename, "r") as file:
        for i, line in enumerate(file.readlines()):
            try:
                instruction = parse_assembly_line(line.strip())
            except Exception as e:
                raise Exception(f"Invalid syntax at line {i}: '{line.strip()}'") from e
            program.append(instruction)
    print(f"Loaded program ({len(program)} instructions)")
    return program


def save_program_to_assembly_file(program: List[Instruction], filename: str):
    print(f"Saving program to {filename}")
    with open(filename, "w") as file:
        for instruction in program:
            file.write(str(instruction) + "\n")
    print(f"Saved program ({len(program)} instructions)")
    return program


def parse_assembly_line(line: str) -> Instruction:
    tokens = line.split()
    return parse_instruction_tokens(tokens)


def parse_instruction_tokens(tokens: List[str]) -> Instruction:
    try:
        cls = [cls for cls in INSTRUCTION_CLASSES if cls.assembly_name() == tokens[0]][0]
        return cls.decode_assembly(tokens)
    except Exception as e:
        raise ValueError(f"Failed to parse instruction from tokens {tokens}") from e

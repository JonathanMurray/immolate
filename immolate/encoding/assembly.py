import re
from pathlib import Path
from typing import List, Dict, Tuple, Optional

from immolate.instructions import Instruction
from immolate.instructions.classes import INSTRUCTION_CLASSES


def save_program_to_file(program: List[Instruction], filename: str):
    print(f"Saving program to {filename}")
    with open(filename, "w") as file:
        for instruction in program:
            file.write(str(instruction) + "\n")
    print(f"Saved program ({len(program)} instructions)")
    return program


def load_sprite_from_file(filename: str) -> bytes:
    with open(filename, "rb") as file:
        return file.read()


def load_from_file(filename: str) -> Tuple[List[bytes], List[Instruction]]:
    print(f"Loading program from {filename}")
    with open(filename, "r") as file:
        lines = file.readlines()
        lines = [line.strip() for line in lines]

        if lines[0] == ".sprites" and ".program" in lines:
            sprite_paths = lines[1: lines.index(".program")]
            parent = Path(filename).parent
            sprites = [load_sprite_from_file(parent.joinpath(p)) for p in sprite_paths]
            program = parse_program(lines[lines.index(".program") + 1:])
        elif lines[0] == ".program" and ".sprites" not in lines:
            sprites = []
            program = parse_program(lines[1:])
        elif ".sprites" not in lines and ".program" not in lines:
            sprites = []
            program = parse_program(lines)
        else:
            raise ValueError("Invalid layout of assembly file")

    print(f"Loaded program ({len(program)} instructions)")
    return sprites, program


def parse_program(lines: List[str]) -> List[Instruction]:
    labels = parse_labels(lines)
    return parse_instructions(lines, labels)


def parse_instructions(lines: List[str], labels: Dict[str, Tuple[int, int]]):
    program = []
    label_line_indices = [line_index for (_, line_index) in labels.values()]
    label_destinations = {label: instruction_index for (label, (instruction_index, _)) in labels.items()}
    for i, line in enumerate(lines):
        if i not in label_line_indices:
            if line != "" and not line.startswith("#"):
                try:
                    instruction = parse_assembly_line(line, label_destinations)
                except Exception as e:
                    raise Exception(f"Invalid syntax at line {i} ('{line}'): {e}") from e
                program.append(instruction)
    return program


def parse_labels(lines: List[str]) -> Dict[str, Tuple[int, int]]:
    labels = {}
    instruction_index = 0
    for line_index, line in enumerate(lines):
        label = try_parse_label(line)
        if label:
            labels[label] = (instruction_index, line_index)
        elif line != "" and not line.startswith("#"):
            instruction_index += 1
    return labels


def try_parse_label(line: str) -> Optional[str]:
    tokens = line.split()

    if len(tokens) >= 1 and re.match("[a-zA-Z]+:", tokens[0]):
        return tokens[0][:-1]


def parse_assembly_line(line: str, labels: Dict[str, int]) -> Instruction:
    tokens = line.split()
    return parse_instruction_tokens(tokens, labels)


def parse_instruction_tokens(tokens: List[str], labels: Dict[str, int]) -> Instruction:
    try:
        class_match = [cls for cls in INSTRUCTION_CLASSES if cls.assembly_name() == tokens[0]]
        if not class_match:
            raise ValueError(f"No class found for {tokens[0]}")
        cls = class_match[0]
        return cls.decode_assembly(tokens, labels)
    except Exception as e:
        raise ValueError(f"Failed to parse instruction from tokens {tokens}: {e}") from e

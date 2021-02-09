import re
from typing import List, Dict, Tuple, Optional

from immolate.encoding.binary import INSTRUCTION_CLASSES
from immolate.instructions import Instruction


def save_program_to_file(program: List[Instruction], filename: str):
    print(f"Saving program to {filename}")
    with open(filename, "w") as file:
        for instruction in program:
            file.write(str(instruction) + "\n")
    print(f"Saved program ({len(program)} instructions)")
    return program


def load_program_from_file(filename: str) -> List[Instruction]:
    print(f"Loading program from {filename}")
    with open(filename, "r") as file:
        lines = file.readlines()
        labels = parse_labels(lines)
        program = parse_instructions(lines, labels)
    print(f"Loaded program ({len(program)} instructions)")
    return program


def parse_instructions(lines: List[str], labels: Dict[str, Tuple[int, int]]):
    program = []
    label_line_indices = [line_index for (_, line_index) in labels.values()]
    label_destinations = {label: instruction_index for (label, (instruction_index, _)) in labels.items()}
    for i, line in enumerate(lines):
        if i not in label_line_indices:
            try:
                instruction = parse_assembly_line(line.strip(), label_destinations)
            except Exception as e:
                raise Exception(f"Invalid syntax at line {i} ('{line.strip()}'): {e}") from e
            program.append(instruction)
    return program


def parse_labels(lines: List[str]) -> Dict[str, Tuple[int, int]]:
    labels = {}
    instruction_index = 0
    for line_index, line in enumerate(lines):
        label = try_parse_label(line.strip())
        if label:
            labels[label] = (instruction_index, line_index)
        else:
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
        cls = [cls for cls in INSTRUCTION_CLASSES if cls.assembly_name() == tokens[0]][0]
        return cls.decode_assembly(tokens, labels)
    except Exception as e:
        raise ValueError(f"Failed to parse instruction from tokens {tokens}: {e}") from e

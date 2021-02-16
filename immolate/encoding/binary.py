from typing import List, Tuple

from immolate.instructions import Instruction
from immolate.instructions.classes import INSTRUCTION_CLASSES

MAGIC_WORD = b"immolate"


def debug(text: str):
    # Change this to toggle debug logging
    show_debug_logs = False
    if show_debug_logs:
        print(text)


def decode_instruction(b: bytes) -> Instruction:
    instruction_type_index: int = b[0]
    payload = b[1:3]
    return INSTRUCTION_CLASSES[instruction_type_index].decode(payload)


def encode_instruction(instruction: Instruction) -> bytes:
    class_index = INSTRUCTION_CLASSES.index(type(instruction))
    encoded_payload = bytes(instruction)
    if len(encoded_payload) != 2:
        raise ValueError(f"Encoded instruction payload must be exactly 2 bytes long, but got {encoded_payload}")
    return bytes([class_index]) + encoded_payload


def save_program_to_file(program: List[Instruction], sprites: List[bytes], filename: str):
    debug(f"Saving program to {filename}")
    with open(filename, "wb") as file:
        file.write(MAGIC_WORD)
        program_bytes = bytes()
        for instruction in program:
            program_bytes += encode_instruction(instruction)
        file.write(len(program_bytes).to_bytes(2, byteorder="big"))
        file.write(program_bytes)
        for sprite in sprites:
            if len(sprite) > 2 ** 16:
                raise ValueError(f"Too large sprite. Byte size: {len(sprite)}")
            file.write(len(sprite).to_bytes(2, "big"))
            file.write(sprite)
    debug("Saved.")


def load_program_from_file(filename: str) -> Tuple[List[Instruction], List[bytes]]:
    debug(f"Reading program from {filename}")
    program = []
    sprites = []
    with open(filename, "rb") as file:
        first_part = file.read(len(MAGIC_WORD))
        if first_part != MAGIC_WORD:
            raise Exception(f"Invalid executable file. Expected magic string '{MAGIC_WORD}' but got '{first_part}'")
        program_section_size = int.from_bytes(file.read(2), byteorder="big")
        program_section_end = file.tell() + program_section_size
        while file.tell() < program_section_end:
            chunk = file.read(3)
            if len(chunk) < 3:
                raise Exception(f"File ended unexpectedly. Last read bytes: {chunk}")
            instruction = decode_instruction(chunk)
            program.append(instruction)
        debug(f"Read {len(program)} instructions.")

        while True:
            sprite_size = file.read(2)
            if len(sprite_size) == 0:
                break
            if len(sprite_size) < 2:
                raise Exception(f"File ended unexpectedly. Last read bytes: {sprite}")
            sprite_size = int.from_bytes(sprite_size, byteorder="big")
            sprite = file.read(sprite_size)
            if len(sprite) < sprite_size:
                raise Exception(f"File ended unexpectedly. Last read bytes: {sprite}")
            sprites.append(sprite)

    return program, sprites

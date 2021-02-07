from typing import List, Type

from immolate.emulator import Put, Add, AddRegisterAndNumber, Jump, JumpIfEqual, Exit, PrintRegister, Instruction

INSTRUCTION_CLASSES: List[Type[Instruction]] = [Put, Add, AddRegisterAndNumber, Jump, JumpIfEqual, Exit, PrintRegister]
MAGIC_WORD = b"immolate"


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


def save_program_to_file(program: List[Instruction], filename: str):
    print(f"Saving program to {filename}")
    with open(filename, "wb") as file:
        file.write(MAGIC_WORD)
        for instruction in program:
            b = encode_instruction(instruction)
            file.write(b)
    print("Saved.")


def load_program_from_file(filename: str) -> List[Instruction]:
    print(f"Reading program from {filename}")
    program = []
    with open(filename, "rb") as file:
        first_part = file.read(len(MAGIC_WORD))
        if first_part != MAGIC_WORD:
            raise Exception(f"Invalid executable file. Expected magic string '{MAGIC_WORD}' but got '{first_part}'")
        while True:
            chunk = file.read(3)
            if len(chunk) == 0:
                break
            elif len(chunk) != 3:
                raise Exception(f"File ended unexpectedly. Last read bytes: {chunk}")
            program.append(decode_instruction(chunk))
    print(f"Read {len(program)} instructions.")
    return program

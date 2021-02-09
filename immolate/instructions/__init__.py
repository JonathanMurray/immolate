from abc import ABCMeta, abstractmethod
from typing import List, Dict


class Instruction(metaclass=ABCMeta):
    @abstractmethod
    def execute(self, cpu):
        pass

    @staticmethod
    @abstractmethod
    def decode(b: bytes):
        pass

    @abstractmethod
    def __bytes__(self) -> bytes:
        pass

    @staticmethod
    @abstractmethod
    def decode_assembly(tokens: List[str], labels: Dict[str, int]):
        pass

    @staticmethod
    @abstractmethod
    def assembly_name() -> str:
        pass


def _assert_arrow(token: str):
    if token != "<-":
        raise ValueError(f"Expected '<-' but got '{token}'")


def _parse_register(token: str) -> int:
    if not token.startswith("r"):
        raise ValueError(f"Expected register token but got '{token}'")
    return int(token[1:])


def _parse_jump_destination(destination: str, labels: Dict[str, int]):
    try:
        instruction_index = int(destination)
    except ValueError:
        if destination in labels:
            instruction_index = labels[destination]
        else:
            raise ValueError(f"Unknown jump destination: {destination}")
    return instruction_index

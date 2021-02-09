from dataclasses import dataclass
from typing import List, Dict

from immolate.cpu import Cpu
from immolate.instructions import Instruction


@dataclass
class Sleep(Instruction):
    millis: int  # 16

    def execute(self, cpu: Cpu):
        cpu.sleep(self.millis)

    @staticmethod
    def decode(b: bytes):
        millis = int.from_bytes(b[0:2], byteorder="big")
        return Sleep(millis)

    def __bytes__(self) -> bytes:
        return self.millis.to_bytes(2, byteorder="big")

    @staticmethod
    def decode_assembly(tokens: List[str], labels: Dict[str, int]):
        millis = int(tokens[1])
        return Sleep(millis)

    def __str__(self):
        return f"{self.assembly_name()} {self.millis}"

    @staticmethod
    def assembly_name() -> str:
        return "SLEEP"

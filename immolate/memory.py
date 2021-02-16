from typing import List


class Memory:
    def __init__(self, sprites: List[bytes] = None):
        self._ram = [0] * 255
        self.sprites = sprites or []

    def __setitem__(self, address: int, value: int):
        self._ram[address] = value

    def __getitem__(self, address) -> int:
        return self._ram[address]

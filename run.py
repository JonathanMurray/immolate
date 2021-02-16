#!/usr/bin/env python3
import sys
from typing import List

from immolate.cpu import Cpu
from immolate.encoding import binary
from immolate.memory import Memory
from immolate.runner import run_program
from immolate.screen import PygameScreen


def run_program_from_file(filename: str, program_args: List[int]):
    program, sprites = binary.load_program_from_file(filename)
    memory = Memory(sprites=sprites)
    screen = PygameScreen(memory)
    cpu = Cpu(program, args=program_args, allow_sleeps=True, screen=screen, memory=memory)
    run_program(cpu)


def main():
    argv = sys.argv
    if len(argv) < 2 or len(argv) > 6:
        print(f"USAGE: {argv[0]} <FILE> [<ARGS>]\nExecute program from <FILE>")
        return
    filename = argv[1]
    program_args = [int(a) for a in argv[2:]]
    run_program_from_file(filename, program_args)


if __name__ == '__main__':
    main()

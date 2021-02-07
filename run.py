#!/usr/bin/env python3
import sys
from typing import List

from immolate.emulator import Cpu
from immolate.encoding import load_program_from_file


def run_program_from_file(filename: str, program_args: List[int]):
    program = load_program_from_file(filename)
    cpu = Cpu(program, args=program_args)
    cpu.run_until_exit()
    print(f"Program exited with code {cpu.exit_code}")
    print(f"Output: {cpu.output}")


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

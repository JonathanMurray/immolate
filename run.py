#!/usr/bin/env python3
import sys

from immolate.emulator import Cpu
from immolate.encoding import load_program_from_file


def run_program_from_file(filename: str):
    program = load_program_from_file(filename)
    cpu = Cpu(program)
    cpu.run_until_exit()
    print(f"Program exited with code {cpu.exit_code}")
    print(f"Output: {cpu.output}")


def main():
    argv = sys.argv
    if len(argv) != 2:
        print(f"USAGE: {argv[0]} <FILE>\nExecute program from <FILE>")
        return
    filename = argv[1]
    run_program_from_file(filename)


if __name__ == '__main__':
    main()

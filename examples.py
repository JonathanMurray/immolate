#!/usr/bin/env python3
import sys
from typing import List

from immolate.emulator import Cpu
from immolate.example_programs import EXAMPLE_PROGRAMS


def run_example(name: str, program_args: List[int]):
    program = EXAMPLE_PROGRAMS[name]
    print(f"Running example program '{name}' ({len(program)} instructions long)")
    cpu = Cpu(program, args=program_args)
    print(cpu)
    cpu.run_until_exit()
    print(cpu)
    print(f"Program exited with code {cpu.exit_code}")
    print(f"Output: {cpu.output}")


def main():
    argv = sys.argv
    valid_programs = list(EXAMPLE_PROGRAMS.keys())
    if len(argv) < 2 or len(argv) > 6:
        print(f"USAGE: {argv[0]} <PROGRAM> [<ARGS>]\nExecute example program\nValid examples: {valid_programs}")
        return
    program_name = argv[1]
    if program_name not in EXAMPLE_PROGRAMS:
        print(f"Invalid program: {program_name}")
        print(f"Valid programs are: {valid_programs}")
        return

    program_args = [int(a) for a in argv[2:]]

    run_example(program_name, program_args)


if __name__ == '__main__':
    main()

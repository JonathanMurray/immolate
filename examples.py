#!/usr/bin/env python3
import sys

from immolate.emulator import Cpu
from immolate.example_programs import EXAMPLE_PROGRAMS


def run_example(name: str):
    program = EXAMPLE_PROGRAMS[name]
    print(f"Running example program '{name}' ({len(program)} instructions long)")
    cpu = Cpu(program)
    print(cpu)
    cpu.run_until_exit()
    print(cpu)
    print(f"Program exited with code {cpu.exit_code}")
    print(f"Output: {cpu.output}")


def main():
    argv = sys.argv
    valid_programs = list(EXAMPLE_PROGRAMS.keys())
    if len(argv) != 2:
        print(f"USAGE: {argv[0]} <PROGRAM>\nExecute example program\nValid examples: {valid_programs}")
        return
    program_name = argv[1]
    if program_name not in EXAMPLE_PROGRAMS:
        print(f"Invalid program: {program_name}")
        print(f"Valid programs are: {valid_programs}")
        return

    run_example(program_name)


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
import sys

from immolate.assembler import load_program_from_assembly_file, save_program_to_assembly_file
from immolate.encoding import save_program_to_file, load_program_from_file


def assemble(executable_filename: str, assembly_filename: str):
    program = load_program_from_file(executable_filename)
    save_program_to_assembly_file(program, assembly_filename)


def main():
    argv = sys.argv
    if len(argv) != 3:
        print(f"USAGE: {argv[0]} <EXECUTABLE> <ASSEMBLY>\nGenerate assembly file from executable file")
        return
    executable_filename = argv[1]
    assembly_filename = argv[2]
    assemble(executable_filename, assembly_filename)


if __name__ == '__main__':
    main()

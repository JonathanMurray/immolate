#!/usr/bin/env python3
import sys

from immolate.assembler import load_program_from_assembly_file
from immolate.encoding import save_program_to_file


def assemble(assembly_filename: str, executable_filename: str):
    program = load_program_from_assembly_file(assembly_filename)
    save_program_to_file(program, executable_filename)


def main():
    argv = sys.argv
    if len(argv) != 3:
        print(f"USAGE: {argv[0]} <ASSEMBLY> <EXECUTABLE>\nGenerate executable file from assembly file")
        return
    assembly_filename = argv[1]
    executable_filename = argv[2]
    assemble(assembly_filename, executable_filename)


if __name__ == '__main__':
    main()

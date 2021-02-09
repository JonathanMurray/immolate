#!/usr/bin/env python3
import sys

from immolate.encoding import assembly, binary


def assemble(assembly_filename: str, executable_filename: str):
    program = assembly.load_program_from_file(assembly_filename)
    binary.save_program_to_file(program, executable_filename)


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

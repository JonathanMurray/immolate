#!/usr/bin/env python3
import sys

from immolate.encoding import assembly, binary


def disassemble(executable_filename: str, assembly_filename: str):
    # TODO handle sprites correctly
    program, sprites = binary.load_program_from_file(executable_filename)
    assembly.save_program_to_file(program, assembly_filename)


def main():
    argv = sys.argv
    if len(argv) != 3:
        print(f"USAGE: {argv[0]} <EXECUTABLE> <ASSEMBLY>\nGenerate assembly file from executable file")
        return
    executable_filename = argv[1]
    assembly_filename = argv[2]
    disassemble(executable_filename, assembly_filename)


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
import sys

from immolate.encoding import binary


def parse_program_in_file(filename: str):
    program = binary.load_program_from_file(filename)
    for i, instruction in enumerate(program):
        print(f"{i}: {instruction}")


def main():
    argv = sys.argv
    if len(argv) != 2:
        print(f"USAGE: {argv[0]} <FILE>\nParse program in <FILE>")
        return
    filename = argv[1]
    parse_program_in_file(filename)


if __name__ == '__main__':
    main()

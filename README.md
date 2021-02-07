# Immolate

_An emulator, assembler and file-format for a very simplified made-up processor instruction set._

## Using it

```bash
# Create an assembly file that contains a valid program
echo "EXIT 0" > my_program.txt

# Turn the program into code that the emulator can run
./assemble.py my_program.txt my_program

# Run the program
./run.py my_program
```

For a (slightly) larger example program, see [fibonacci](files/fibonacci_assembly.txt)

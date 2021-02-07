from typing import List, Dict

from immolate.emulator import Put, Add, AddRegisterAndNumber, Jump, JumpIfEqual, Exit, PrintRegister, Instruction

FIBONACCI = [
    PrintRegister(0),  # Print fib(0)
    Put(1, 0),  # Prepare fib(1)
    PrintRegister(0),  # Print fib(1)
    Put(5, 2),  # Limit the number of loops
    Add(0, 1, 1),  # Compute fib(n)
    PrintRegister(1),  # Print fib(n)
    Add(0, 1, 0),  # Compute fib(n+1)
    PrintRegister(0),  # Print fib(n+1)
    AddRegisterAndNumber(1, 3, 3),  # Increment loop counter
    JumpIfEqual(2, 3, 11),  # Exit if we've run enough loops
    Jump(4),  # Otherwise run the loop again
    Exit(0),  # Exit
]

PRINT_1337 = [
    Put(1, 0),
    PrintRegister(0),
    Put(3, 0),
    PrintRegister(0),
    PrintRegister(0),
    Put(7, 0),
    PrintRegister(0),
    Exit(0),
]

EXAMPLE_PROGRAMS: Dict[str, List[Instruction]] = {
    "fib": FIBONACCI,
    "1337": PRINT_1337,
}

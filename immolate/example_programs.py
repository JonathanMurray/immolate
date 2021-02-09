from typing import List, Dict

from immolate.instructions import Instruction
from immolate.instructions.activate_screen import ActivateScreen
from immolate.instructions.add import Add
from immolate.instructions.add_register_and_number import AddRegisterAndNumber
from immolate.instructions.breakpoint import Breakpoint
from immolate.instructions.exit import Exit
from immolate.instructions.fill_screen import FillScreen
from immolate.instructions.jump import Jump
from immolate.instructions.jump_if_equal import JumpIfEqual
from immolate.instructions.print_register import PrintRegister
from immolate.instructions.put import Put
from immolate.instructions.refresh_screen import RefreshScreen
from immolate.instructions.sleep import Sleep

FIBONACCI = [
    PrintRegister(0),  # Print fib(0)
    Sleep(250),
    Put(1, 0),  # Prepare fib(1)
    PrintRegister(0),  # Print fib(1)
    Sleep(250),
    Put(5, 2),  # Limit the number of loops
    Add(0, 1, 1),  # Compute fib(n)
    PrintRegister(1),  # Print fib(n)
    Sleep(250),
    Add(0, 1, 0),  # Compute fib(n+1)
    PrintRegister(0),  # Print fib(n+1)
    Sleep(250),
    AddRegisterAndNumber(1, 3, 3),  # Increment loop counter
    JumpIfEqual(2, 3, 15),  # Exit if we've run enough loops
    Jump(6),  # Otherwise run the loop again
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

ADD_TWO_ARGS = [
    Add(0, 1, 2),
    PrintRegister(2),
    Exit(0)
]

GRAPHICS = [
    ActivateScreen(),  # Show graphics
    Put(255, 1),  # Stop when we've reached the color value 255
    FillScreen(0),  # Fill screen
    RefreshScreen(),  # Refresh screen
    AddRegisterAndNumber(1, 0, 0),  # Increment color value
    JumpIfEqual(0, 1, 7),  # Exit if we've reached 255
    Jump(2),  # Otherwise, repeat the loop
    Exit(0)  # Exit
]

BREAKPOINT = [
    Put(1, 0),
    PrintRegister(0),
    Breakpoint(),
    Put(2, 0),
    PrintRegister(0),
    Exit(0)
]

EXAMPLE_PROGRAMS: Dict[str, List[Instruction]] = {
    "fib": FIBONACCI,
    "1337": PRINT_1337,
    "add": ADD_TWO_ARGS,
    "graphics": GRAPHICS,
    "breakpoint": BREAKPOINT,
}

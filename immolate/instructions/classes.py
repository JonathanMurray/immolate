from typing import List, Type

from immolate.instructions import Instruction
from immolate.instructions.activate_screen import ActivateScreen
from immolate.instructions.add import Add
from immolate.instructions.add_register_and_number import AddRegisterAndNumber
from immolate.instructions.breakpoint import Breakpoint
from immolate.instructions.exit import Exit
from immolate.instructions.jump import Jump
from immolate.instructions.jump_if_equal import JumpIfEqual
from immolate.instructions.memory import Store, Load
from immolate.instructions.print_register import PrintRegister
from immolate.instructions.put import Put
from immolate.instructions.refresh_screen import RefreshScreen
from immolate.instructions.sleep import Sleep
from immolate.instructions.stack import Push, Pop
from immolate.instructions.subroutine import CallSubroutine, Return

INSTRUCTION_CLASSES: List[Type[Instruction]] = [Put, Add, AddRegisterAndNumber, Jump, JumpIfEqual, Exit, PrintRegister,
                                                Sleep, ActivateScreen, RefreshScreen, Breakpoint, Push, Pop,
                                                CallSubroutine, Return, Store, Load]

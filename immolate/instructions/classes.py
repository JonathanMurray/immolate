from typing import List, Type

from immolate.instructions import Instruction
from immolate.instructions.activate_screen import ActivateScreen
from immolate.instructions.add import Add
from immolate.instructions.add_register_and_number import AddRegisterAndNumber
from immolate.instructions.breakpoint import Breakpoint
from immolate.instructions.exit import Exit
from immolate.instructions.fill_screen import FillScreen
from immolate.instructions.jump import Jump
from immolate.instructions.jump_if_equal import JumpIfEqual
from immolate.instructions.pop import Pop
from immolate.instructions.print_register import PrintRegister
from immolate.instructions.push import Push
from immolate.instructions.put import Put
from immolate.instructions.refresh_screen import RefreshScreen
from immolate.instructions.sleep import Sleep

INSTRUCTION_CLASSES: List[Type[Instruction]] = [Put, Add, AddRegisterAndNumber, Jump, JumpIfEqual, Exit, PrintRegister,
                                                Sleep, ActivateScreen, RefreshScreen, FillScreen, Breakpoint, Push, Pop]

from immolate.emulator import Cpu


def run_program(cpu: Cpu):
    try:
        while True:
            cpu.run_until_exit_or_halt()
            if cpu.has_exited:
                print(f"Program exited with code {cpu.exit_code}")
                return
            if cpu.halted:
                print(f"Program halted at {cpu.instruction_pointer}")
                print_debugger_help()
                while cpu.halted:
                    choice = input("> ")
                    if choice.startswith("1"):
                        cpu.halted = False
                    elif choice.startswith("2"):
                        cpu.run_one_cycle()
                        if cpu.has_exited:
                            print(f"Program exited with code {cpu.exit_code}")
                            return
                    elif choice.startswith("3"):
                        print(cpu.dump())
                    else:
                        print_debugger_help()
    except Exception as e:
        raise Exception(f"Program crashed: {e}") from e


def print_debugger_help():
    print("- - - - - - - - - -")
    print("Resume execution (1)")
    print("Step one instruction (2)")
    print("Dump CPU (3)")

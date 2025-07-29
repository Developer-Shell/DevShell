from shell import *
import os

if __name__ == "__main__":
    shell = Shell("DevShell")
    closed = False
    while not closed:
        command = input("devshell v1 > ").strip().split(" ")

        if command[0].strip().lower() == "install":
            shell.install(os.getcwd(), command[1])

        if command[0].strip() == "":
            continue
        name = command[0]
        args = None
        if len(command) > 1:
            args = command[1:]
            for arg in args:
                args[args.index(arg)] = f"\"{arg}\""
        shell.execute([name, args])

import os
import subprocess

import shellingham


class ShellInfo:
    def __init__(self, path: str, name: str):
        self.path: str = path
        self.name: str = name


def getShell():
    shellPath: str
    shellName: str

    try:
        shellName, shellPath = shellingham.detect_shell()
    except shellingham.ShellDetectionFailure:
        if os.name == "posix":
            shellName, shellPath = ("unknown_posix", os.environ["SHELL"])
        elif os.name == "nt":
            shellName, shellPath = ("unknown_nt", os.environ["COMSPEC"])
        else:
            raise NotImplementedError(f"OS {os.name!r} is not supported :c")
    return ShellInfo(shellPath, shellName)


def getCommandSeparatorForShellName(shellName: str):
    match shellName:
        case "powershell":
            return ";"
        case "unknown_posix":
            return ";"
        case "unknown_nt":
            return "&&"


class ComputerProcess:
    # yeah this should be called ShellProcess
    # but isn't "Computer" more whimsical?

    def __init__(self):
        self.shell: ShellInfo = getShell()
        self.stashedCommands: list[str] = []

    def run(self, command: str):
        """
        Runs a command in a new process.
        """
        output = subprocess.run(
            [self.shell.path, command], text=True, capture_output=True
        )

        print(output)
        if output.returncode != 0:
            raise Exception("Error: ", output)

    def stashCommand(self, command: str):
        """
        Adds a command to self.stashedCommands.
        """
        self.stashedCommands.append(command)

    def clearStashedCommands(self):
        """
        Resets self.stashedCommands.
        """
        self.stashedCommands = []

    def runStashedCommands(self):
        """
        Runs all commands in self.stashedCommands, all in
        one "line".
        """

        longCommand = f"{getCommandSeparatorForShellName(self.shell.name)} ".join(
            self.stashedCommands
        )
        print(longCommand)

        self.run(longCommand)


computerProcess = ComputerProcess()

print(computerProcess.shell.name)

computerProcess.stashCommand('echo "Hello, world" > hii.txt')
computerProcess.stashCommand('echo "Greetings" > salutations.txt')

computerProcess.runStashedCommands()

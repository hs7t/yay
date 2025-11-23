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
        shellPath, shellName = shellingham.detect_shell()
    except shellingham.ShellDetectionFailure:
        if os.name == "posix":
            shellPath, shellName = ("unknown", os.environ["SHELL"])
        elif os.name == "nt":
            shellPath, shellName = ("unknown", os.environ["COMSPEC"])
        else:
            raise NotImplementedError(f"OS {os.name!r} is not supported :c")
    return ShellInfo(shellPath, shellName)


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
        output = subprocess.run(command, shell=True, text=True, capture_output=True)

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

        longCommand = f" {os.linesep}".join(self.stashedCommands)
        print(longCommand)

        self.run(longCommand)


computerProcess = ComputerProcess()

computerProcess.stashCommand('echo "Hello, world" > hii.txt')
computerProcess.stashCommand('echo "Greetings" > salutations.txt')

computerProcess.runStashedCommands()

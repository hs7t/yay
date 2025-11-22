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


class Computer:
    # yeah this should be called Shell
    # but isn't "Computer" more whimsical?

    def __init__(self):
        self.shell: ShellInfo = getShell()
        self.stashedCommands: list[str] = []
        self.process = subprocess.Popen(
            [self.shell.path], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True
        )

    def run(self, command: str):
        """
        Runs a command in self.process.
        """
        (output, error) = self.process.communicate(input=command)
        if error:
            raise Exception("Error in terminal")

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
        Runs all commands in self.stashedCommands, one after the
        other, in self.process.
        """
        for command in self.stashedCommands:
            self.run(command)

    def murder(self):
        """
        Kills self.process. Ouch.
        """
        self.process.kill()


computer = Computer()

computer.stashCommand('echo "Hello, world" > hii.txt')
computer.stashCommand('echo "Greetings" > salutation.txt')

computer.runStashedCommands()

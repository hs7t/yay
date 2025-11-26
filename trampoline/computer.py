import os
import subprocess
from enum import Enum, auto

import shellingham


class ShellType(Enum):
    PowerShell = auto()
    Bash = auto()
    ZShell = auto()
    GenericPOSIX = auto()
    WindowsCommandPrompt = auto()


class ShellInfo:
    def __init__(self, path: str, name: ShellType):
        self.path: str = path
        self.type: ShellType = name


def getShell():
    shellPath: str
    shellType: ShellType

    try:
        shellName, shellPath = shellingham.detect_shell()

        match shellName:
            case "powershell":
                shellType = ShellType.PowerShell
            case "bash":
                shellType = ShellType.Bash
            case "cmd":
                shellType = ShellType.WindowsCommandPrompt
            case "zsh":
                shellType = ShellType.ZShell
            case _:
                raise shellingham.ShellDetectionFailure
    except shellingham.ShellDetectionFailure:
        if os.name == "posix":
            shellType, shellPath = (ShellType.GenericPOSIX, os.environ["SHELL"])
        elif os.name == "nt":
            shellType, shellPath = (
                ShellType.WindowsCommandPrompt,
                os.environ["COMSPEC"],
            )
        else:
            raise NotImplementedError(f"OS {os.name!r} is not supported :c")
    return ShellInfo(shellPath, shellType)


from computer import ShellType


class MultiShellCommand:
    def __init__(
        self, powerShell, bash, zShell, genericPosix, windowsCommandPrompt
    ) -> None:
        self._powerShell = powerShell
        self._bash = bash
        self._zShell = zShell
        self._genericPosix = genericPosix
        self._windowsCommandPrompt = windowsCommandPrompt

    def getForShellType(self, shellType: ShellType):
        match shellType:
            case ShellType.PowerShell:
                return self._powerShell
            case ShellType.Bash:
                return self._bash
            case ShellType.ZShell:
                return self._zShell
            case ShellType.GenericPOSIX:
                return self._genericPosix
            case ShellType.WindowsCommandPrompt:
                return self._windowsCommandPrompt


def getCommandSeparatorForShellType(shellType: ShellType):
    match shellType:
        case (
            ShellType.PowerShell
            | ShellType.ZShell
            | ShellType.Bash
            | ShellType.GenericPOSIX
        ):
            return ";"
        case ShellType.WindowsCommandPrompt:
            return "&&"  # why, windows. why.


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

        match self.shell.type:
            case ShellType.PowerShell:
                output = subprocess.run(
                    [self.shell.path, "-Command", command], text=True, capture_output=True
                )
            case ShellType.WindowsCommandPrompt:
                output = subprocess.run(
                    [self.shell.path, "/c", command], text=True, capture_output=True
                )
            case ShellType.Bash | ShellType.ZShell | ShellType.GenericPOSIX | _:
                output = subprocess.run(
                    [self.shell.path, "-c", command], text=True, capture_output=True
                )

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

        longCommand = f"{getCommandSeparatorForShellType(self.shell.type)} ".join(
            self.stashedCommands
        )
        print(longCommand)

        self.run(longCommand)

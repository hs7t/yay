from computer import ShellType

class MultiShellCommand:
    def __init__(self, powerShell, bash, zShell, genericPosix, windowsCommandPrompt) -> None:
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
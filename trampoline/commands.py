from computer import ShellType


def formatStringForShell(shellType, string):
    match shellType:
        case ShellType.PowerShell:
            return '"' + string.replace('"', '`"').replace("'", "`'") + '"'
        case ShellType.Bash | ShellType.GenericPOSIX | ShellType.ZShell:
            if "'" in string:
                return "'" + string.replace("'", "'\\''") + "'"
            else:
                return "'" + string + "'"
        case ShellType.WindowsCommandPrompt:
            return string.replace('"', '""').replace("%", "%%")


def c_print(shellType, string):
    match shellType:
        case ShellType.PowerShell:
            return f"Write-Host {formatStringForShell(shellType, string)}"
        case ShellType.Bash | ShellType.GenericPOSIX | ShellType.ZShell:
            return f"printf {formatStringForShell(shellType, string)}"
        case ShellType.WindowsCommandPrompt:
            return f"echo {formatStringForShell(shellType, string)}"


def c_navto(shellType, path: str):
    match shellType:
        case ShellType.PowerShell:
            return f"Set-Location {path}"
        case (
            ShellType.Bash
            | ShellType.GenericPOSIX
            | ShellType.ZShell
            | ShellType.WindowsCommandPrompt
        ):
            return f"cd {path}"


def c_clone(shellType, url: str):
    match shellType:
        case (
            ShellType.Bash
            | ShellType.GenericPOSIX
            | ShellType.ZShell
            | ShellType.WindowsCommandPrompt
        ):
            return f"git clone {formatStringForShell(shellType, string=url)}"

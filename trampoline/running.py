from computer import MultiShellCommand

COMMANDS = {
    "print": MultiShellCommand (
        powerShell="echo \"{string}\"",
        bash="echo \"{string}\"",
        zShell="echo \"{string}\"",
        genericPosix="echo \"{string}\"",
        windowsCommandPrompt="echo \"{string}\""
    )
}
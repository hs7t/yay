import commands
from computer import ComputerProcess, ShellType
from parsing import CommandType, Instruction, ReferenceType


def runInstructions(instructions: list[Instruction]):
    computerProcess = ComputerProcess()
    for instruction in instructions:
        if instruction.commandType is CommandType.Ignore:
            continue
        if (
            instruction.commandType is CommandType.RunAction
            and instruction.referenceType is ReferenceType.Operation
        ):
            command: str = ""
            if instruction.reference == "clone":
                repoURL: str = ""
                for argument in instruction.arguments:
                    if isinstance(argument.value, str):
                        repoURL += argument.value
                command = commands.c_clone(computerProcess.shell.type, repoURL) or ""

            if instruction.reference == "print":
                stringToPrint: str = ""
                for argument in instruction.arguments:
                    if isinstance(argument.value, str):
                        stringToPrint += argument.value
                command = (
                    commands.c_print(computerProcess.shell.type, stringToPrint) or ""
                )

            if instruction.reference == "navto":
                path: str = ""
                for argument in instruction.arguments:
                    if isinstance(argument.value, str):
                        path += argument.value
                command = commands.c_navto(computerProcess.shell.type, path) or ""

            if command == "":
                continue
            else:
                computerProcess.stashCommand(command)

    print(computerProcess.stashedCommands)
    computerProcess.runStashedCommands()

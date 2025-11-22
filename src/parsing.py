from enum import Enum, auto

from typing_extensions import TypedDict, Union

from misc import isNumber
from tokenization import Token, Tokenizer, TokenType


class ParticleType(Enum):
    Command = auto()
    Reference = auto()
    Literal = auto()


class CommandType(Enum):
    SetGlobal = auto()  # %
    RunAction = auto()  # !
    ShellEnter = auto()  # $
    Ignore = auto()  # /


class ReferenceType(Enum):
    Operation = auto()  # like 'print' or 'clone'
    Store = auto()  # such as 'global.name' (or 'name' directly if within SetGlobal)
    Other = auto()


class LiteralType(Enum):
    String = auto()  # like "hello", "t", or "meow meow"
    Number = auto()  # like 5, 2048 or 1.0003


COMMANDTOKENTEXT_COMMANDTYPE_MAP = {
    "%": CommandType.SetGlobal,
    "!": CommandType.RunAction,
    "$": CommandType.ShellEnter,
    "/": CommandType.Ignore,
}


class ArgumentType(Enum):
    InstructionSet = auto()
    StringLiteral = auto()
    NumberLiteral = auto()
    Reference = auto()


class Argument:
    def __init__(self, type: ArgumentType, value: Union[str, int, list]) -> None:
        self.type: ArgumentType = type
        self.value: Union[str, int, list] = value


class Instruction:
    def __init__(
        self,
        commandType: CommandType,
        referenceType: ReferenceType | None = None,
        reference: str | None = None,
        arguments: list[Argument] = [],
    ):
        self.commandType = commandType
        self.referenceType = referenceType
        self.reference = reference
        self.arguments = arguments


class InstructionConstructionObject(TypedDict):
    commandType: CommandType | None
    referenceType: ReferenceType | None
    referenceValue: str | None
    arguments: list[Argument]
    stringArgumentAccumulation: str | None


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens: list[Token] = tokens

    def getInstructions(self):
        foundInstructions: list[Instruction] = []
        currentInstruction: InstructionConstructionObject | None = None

        stringMode = False

        def addInstruction(instructions, instruction):
            if instruction["stringArgumentAccumulation"]:
                instruction["arguments"].append(
                    Argument(
                        value=instruction["stringArgumentAccumulation"],
                        type=ArgumentType.StringLiteral,
                    )
                )
            instructions.append(
                Instruction(
                    commandType=instruction["commandType"],
                    referenceType=instruction["referenceType"],
                    reference=instruction["referenceValue"],
                    arguments=instruction["arguments"],
                )
            )
            return instructions

        for token in self.tokens:
            # If I run into a command
            if token.type is TokenType.Command:
                # Push old instruction into foundInstructions list
                if currentInstruction is not None and isinstance(
                    currentInstruction["commandType"], CommandType
                ):
                    foundInstructions = addInstruction(
                        foundInstructions, currentInstruction
                    )
                    currentInstruction = None

                # Start a new instruction
                if currentInstruction is None:
                    currentInstruction = {
                        "referenceType": None,
                        "referenceValue": None,
                        "arguments": [],
                        "commandType": COMMANDTOKENTEXT_COMMANDTYPE_MAP[token.text],
                        "stringArgumentAccumulation": None,
                    }

            if not currentInstruction:
                continue

            # If I run into a reference
            if token.type is TokenType.Reference:
                if currentInstruction["commandType"] is CommandType.SetGlobal:
                    currentInstruction["referenceType"] = ReferenceType.Store
                    currentInstruction["referenceValue"] = token.text
                if currentInstruction["commandType"] is CommandType.RunAction:
                    currentInstruction["referenceType"] = ReferenceType.Operation
                    if not currentInstruction["referenceValue"]:
                        currentInstruction["referenceValue"] = token.text
                    else:
                        currentInstruction["arguments"].append(
                            Argument(type=ArgumentType.Reference, value=token.text)
                        )

                if currentInstruction["commandType"] is CommandType.ShellEnter:
                    if currentInstruction["stringArgumentAccumulation"] is None:
                        currentInstruction["stringArgumentAccumulation"] = ""
                    currentInstruction["stringArgumentAccumulation"] += token.text

            # Handle strings
            if token.type is TokenType.StringBlockStart:
                stringMode = True
                currentInstruction["stringArgumentAccumulation"] = None  # just in case

            if stringMode and token.type == TokenType.Literal:
                if not currentInstruction["stringArgumentAccumulation"]:
                    currentInstruction["stringArgumentAccumulation"] = ""

                currentInstruction["stringArgumentAccumulation"] += token.text

            if token.type is TokenType.StringBlockEnd:
                stringMode = False

            if (
                not stringMode
                and token.type == TokenType.Literal
                and isNumber(token.text)
            ):
                currentInstruction["arguments"].append(
                    Argument(type=ArgumentType.NumberLiteral, value=token.text)
                )

        if currentInstruction is not None and isinstance(
            currentInstruction["commandType"], CommandType
        ):
            foundInstructions = addInstruction(foundInstructions, currentInstruction)
        return foundInstructions


tokens = Tokenizer("""
    % yay 0.1
    % title "Example script"
    % revision 1
    % supports "meow"

    / the following line will print the title we set above!
    ! print meta.title

    ! end
    """).getTokens()

print("\n🔠 Raw tokens:")
print([(token.type, token.text) for token in tokens])

instructions = Parser(tokens).getInstructions()

print("\n📋 Instructions:")
for instruction in instructions:
    print(
        "- ",
        [
            instruction.commandType,
            instruction.referenceType,
            instruction.reference,
            [[argument.type, argument.value] for argument in instruction.arguments],
        ],
    )

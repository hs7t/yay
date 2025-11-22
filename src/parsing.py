from enum import Enum, auto
from multiprocessing import Value
from typing import Optional

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

        for token in self.tokens:
            # If I run into a command
            if token.type is TokenType.Command:
                # Start new instruction, push old one to foundInstructions
                if currentInstruction is not None and isinstance(
                    currentInstruction["commandType"], CommandType
                ):
                    if currentInstruction["stringArgumentAccumulation"]:
                        currentInstruction["arguments"].append(
                            Argument(
                                value=currentInstruction["stringArgumentAccumulation"],
                                type=ArgumentType.StringLiteral,
                            )
                        )
                    foundInstructions.append(
                        Instruction(
                            commandType=currentInstruction["commandType"],
                            referenceType=currentInstruction["referenceType"],
                            reference=currentInstruction["referenceValue"],
                            arguments=currentInstruction["arguments"],
                        )
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
                    currentInstruction["referenceValue"] = token.text

                if currentInstruction["commandType"] is CommandType.ShellEnter:
                    if currentInstruction["stringArgumentAccumulation"] is None:
                        currentInstruction["stringArgumentAccumulation"] = ""
                    currentInstruction["stringArgumentAccumulation"] += token.text

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

        return foundInstructions


tokens = Tokenizer("""
    % yay 0.1
    % title "Example script"
    % revision 1
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

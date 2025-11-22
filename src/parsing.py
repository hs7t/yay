from enum import Enum, auto

from typing_extensions import Optional, TypedDict

from tokenization import Token, TokenType


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


class LiteralType(Enum):
    String = auto()  # like "hello", "t", or "meow meow"
    Number = auto()  # like 5, 2048 or 1.0003


COMMANDTOKENTEXT_COMMANDTYPE_MAP = {
    "%": CommandType.SetGlobal,
    "!": CommandType.RunAction,
    "$": CommandType.ShellEnter,
    "/": CommandType.Ignore,
}


class Instruction:
    def __init__(
        self, commandType: CommandType, reference: str, arguments: Optional[list]
    ):
        self.commandType = commandType
        self.reference = reference
        self.arguments = arguments


class InstructionConstructionObject(TypedDict):
    commandType: CommandType | None
    referenceType: ReferenceType | None
    referenceValue: str | None
    arguments: str | None


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens: list[Token] = tokens

    def getInstructions(self):
        foundInstructions: list[Instruction] = []
        currentInstruction: InstructionConstructionObject = {
            "commandType": None,
            "referenceType": None,
            "referenceValue": None,
            "arguments": None,
        }

        for token in self.tokens:
            if token.type is TokenType.Command:
                # Start new instruction, push old one to foundInstructions
                if (
                    currentInstruction
                    and currentInstruction["commandType"]
                    and currentInstruction["referenceType"]
                    and currentInstruction["referenceValue"]
                    and currentInstruction["arguments"]
                ):
                    foundInstructions.append(
                        Instruction(
                            commandType=currentInstruction["commandType"],
                            reference=currentInstruction["reference"],
                            arguments=currentInstruction["arguments"],
                        )
                    )
                    currentInstruction = {
                        "commandType": None,
                        "referenceType": None,
                        "referenceValue": None,
                        "arguments": None,
                    }

                currentInstruction["commandType"] = COMMANDTOKENTEXT_COMMANDTYPE_MAP[
                    token.text
                ]
            pass

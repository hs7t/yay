from enum import Enum, auto
from typing import Literal

class TokenType(Enum):
    Literal = auto()
    Reference = auto()
    Command = auto()

    MultilineBlockStart = auto()
    MultilineBlockEnd = auto()
    StringBlockStart = auto()
    StringBlockEnd = auto()

    SetStart = auto()
    SetEnd = auto()

class Token:
    def __init__(self, type: TokenType, text: str):
        self.type = type
        self.text = text

class CommandType(Enum):
    Run = auto()
    ShellRun = auto()
    GlobalSet = auto()

class LiteralType(Enum):
    Integer = auto()

CHUNK_TOKEN_TYPE_MAP = {
    "commands": {
        "%": TokenType.Command,
        "!": TokenType.Command,
        "$": TokenType.Command,
    },
    "stringBlockStart": {
        '"': TokenType.StringBlockStart,
        "'": TokenType.StringBlockEnd,
    },
    "stringBlockEnd": {
        '"': TokenType.StringBlockEnd,
        "'": TokenType.StringBlockEnd,
    },
    "multilineBlockStart": {
        ":": TokenType.MultilineBlockStart,
    },
    "multilineBlockEnd": {
        ";": TokenType.MultilineBlockEnd,
    },
}

BlockTokenType = Literal[
    TokenType.MultilineBlockStart, 
    TokenType.MultilineBlockEnd,
    TokenType.StringBlockStart,
    TokenType.StringBlockEnd
]

def isNumber(string: str):
    numberable: bool = False
    try:
        int(string)
        numberable = True
    except ValueError:
        pass
    try:
        float(string)
        numberable = True
    except ValueError:
        pass
    try:
        complex(string)
    except ValueError:
        pass

    return numberable


class Tokenizer:
    def __init__ (self, text: str):
        self.text = text
        self.chunks = text.split(" ")
        self.tokens: list[Token] = []

    def getLines(self):
        lines = self.text.splitlines()
        return [line for line in lines if len(line) != 0]

    def getTokens(self):
        blockType: None|BlockTokenType = None
        tokens = []

        for line in self.getLines():
            isFirstChunk = True
            lineTokens: list[Token] = []

            for chunk in line.split(" "):
                if (isFirstChunk):
                    if (chunk in CHUNK_TOKEN_TYPE_MAP['commands']):
                        lineTokens.append(
                            Token(type=TokenType.Command, text=chunk)
                        )
                        continue
                    isFirstChunk = False

                if chunk in CHUNK_TOKEN_TYPE_MAP['multilineBlockStart']:
                    lineTokens.append(
                        Token(type=TokenType.MultilineBlockStart, text=chunk)
                    )
                    blockType = TokenType.MultilineBlockStart
                    continue
                elif chunk in CHUNK_TOKEN_TYPE_MAP['multilineBlockEnd']:
                    lineTokens.append(
                        Token(type=TokenType.MultilineBlockEnd, text=chunk)
                    )
                    blockType = None
                    continue

                if (
                    (chunk in CHUNK_TOKEN_TYPE_MAP['stringBlockStart'])
                    and (blockType is not TokenType.StringBlockStart)
                ):
                    lineTokens.append(
                        Token(type=TokenType.StringBlockStart, text=chunk)
                    )
                    blockType = TokenType.StringBlockStart
                    continue
                elif chunk in CHUNK_TOKEN_TYPE_MAP['stringBlockEnd']:
                    lineTokens.append(
                        Token(type=TokenType.StringBlockEnd, text=chunk)
                    )
                    blockType = None
                    continue

                if (blockType is TokenType.StringBlockStart):
                    lineTokens.append(
                        Token(type=TokenType.Literal, text=chunk)
                    )
                    continue
                elif isNumber(chunk):
                    lineTokens.append(
                        Token(type=TokenType.Literal, text=chunk)
                    )
                    continue
                else:
                    lineTokens.append(
                        Token(type=TokenType.Reference, text=chunk)
                    )
                    continue

            tokens = [*tokens, *lineTokens]
        return tokens

code = """
% yay 0.1
! print " meta title "
"""

tokens: list[Token] = Tokenizer(code).getTokens()
print([[token.type, token.text] for token in tokens])
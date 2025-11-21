from enum import Enum, auto
from typing import Literal
import re

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

def isWhiteSpace(string: str):
    return string.isspace() or len(string) == 0

class Tokenizer:
    def __init__ (self, text: str):
        self.text = text
        self.chunks = text.split(" ")
        self.tokens: list[Token] = []

    def getLines(self):
        lines = self.text.splitlines()
        return [line for line in lines if len(line) != 0]

    def getTokens(self):
        blockStartingTokenType: None|BlockTokenType = None
        tokens = []

        for line in self.getLines():
            isFirstChunkInLine = True
            lineTokens: list[Token] = []

            chunks = re.split(r'(\S+)', line)
            tokenContent = ""

            for chunk in chunks:
                if blockStartingTokenType == None and isWhiteSpace(chunk):
                    continue

                if (isFirstChunkInLine):
                    chunkIsCommand = chunk in CHUNK_TOKEN_TYPE_MAP['commands']
                    if (chunkIsCommand):
                        lineTokens.append(
                            Token(type=TokenType.Command, text=chunk)
                        )
                        continue
                    isFirstChunkInLine = False

                chunkIsMultilineBlockStart = (
                    chunk in CHUNK_TOKEN_TYPE_MAP['multilineBlockStart']
                )
                chunkFirstCharIsMultilineBlockStart = (
                    chunk[0] in CHUNK_TOKEN_TYPE_MAP['multilineBlockStart']
                )

                if (
                    chunkIsMultilineBlockStart 
                    or chunkFirstCharIsMultilineBlockStart
                ):
                    lineTokens.append(
                        Token(type=TokenType.MultilineBlockStart, text=chunk)
                    )
                    blockStartingTokenType = TokenType.MultilineBlockStart
                    continue
                elif (
                    chunk in CHUNK_TOKEN_TYPE_MAP['multilineBlockEnd']
                    or chunk[-1] in CHUNK_TOKEN_TYPE_MAP['multilineBlockEnd']
                ):
                    lineTokens.append(
                        Token(type=TokenType.MultilineBlockEnd, text=chunk)
                    )
                    blockStartingTokenType = None
                    continue
                
                chunkIsStringBlockStart = (
                    chunk in CHUNK_TOKEN_TYPE_MAP['stringBlockStart']
                )
                chunkIsStringBlockEnd = (
                    chunk in CHUNK_TOKEN_TYPE_MAP['stringBlockEnd']
                )

                if (
                    chunkIsStringBlockStart
                    and (blockStartingTokenType is not TokenType.StringBlockStart)
                ):
                    lineTokens.append(
                        Token(type=TokenType.StringBlockStart, text=chunk)
                    )
                    blockStartingTokenType = TokenType.StringBlockStart
                    continue
                elif chunkIsStringBlockEnd:
                    lineTokens.append(
                        Token(type=TokenType.Literal, text=tokenContent)
                    )
                    lineTokens.append(
                        Token(type=TokenType.StringBlockEnd, text=chunk)
                    )

                    blockStartingTokenType = None
                    tokenContent = ""

                    continue

                if (blockStartingTokenType is TokenType.StringBlockStart):
                    tokenContent += chunk
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
! print "meta title"
"""

tokens: list[Token] = Tokenizer(code).getTokens()
print([[token.type, token.text] for token in tokens])
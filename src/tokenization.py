import re
from enum import Enum, auto
from typing import Literal

from misc import isNumber, isWhiteSpace


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


CHUNK_TOKEN_TYPE_MAP = {
    "commands": {
        "%": TokenType.Command,
        "!": TokenType.Command,
        "$": TokenType.Command,
        "/": TokenType.Command,
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
    TokenType.StringBlockEnd,
]


class Tokenizer:
    def __init__(self, text: str):
        self.text = text
        self.chunks = text.split(" ")
        self.tokens: list[Token] = []

    def getLines(self):
        lines = self.text.splitlines()
        return [line for line in lines if len(line) != 0]

    def getTokens(self):
        blockStartingTokenType: None | BlockTokenType = None
        tokens = []

        for line in self.getLines():
            isFirstChunkInLine = True
            lineTokens: list[Token] = []

            chunks = re.split(r"(\S+)", line)
            tokenContent = ""

            for chunk in chunks:
                # not on block? skip whitespace chunks
                if blockStartingTokenType is None and isWhiteSpace(chunk):
                    continue

                # check for commands
                if isFirstChunkInLine:
                    chunkIsCommand = chunk in CHUNK_TOKEN_TYPE_MAP["commands"]
                    if chunkIsCommand:
                        lineTokens.append(Token(type=TokenType.Command, text=chunk))
                        continue
                    isFirstChunkInLine = False

                chunkIsMultilineBlockStart = (
                    chunk in CHUNK_TOKEN_TYPE_MAP["multilineBlockStart"]
                )
                chunkFirstCharIsMultilineBlockStart = (
                    chunk[0] in CHUNK_TOKEN_TYPE_MAP["multilineBlockStart"]
                )

                if chunkIsMultilineBlockStart or chunkFirstCharIsMultilineBlockStart:
                    lineTokens.append(
                        Token(type=TokenType.MultilineBlockStart, text=chunk)
                    )
                    blockStartingTokenType = TokenType.MultilineBlockStart
                    continue
                elif (
                    chunk in CHUNK_TOKEN_TYPE_MAP["multilineBlockEnd"]
                    or chunk[-1] in CHUNK_TOKEN_TYPE_MAP["multilineBlockEnd"]
                ):
                    lineTokens.append(
                        Token(type=TokenType.MultilineBlockEnd, text=chunk)
                    )
                    blockStartingTokenType = None
                    continue

                wholeChunkIsStringBlockStart = (
                    chunk in CHUNK_TOKEN_TYPE_MAP["stringBlockStart"]
                )
                wholeChunkIsStringBlockEnd = (
                    chunk in CHUNK_TOKEN_TYPE_MAP["stringBlockEnd"]
                )

                chunkFirstCharIsStringBlockStart = (
                    chunk[0] in CHUNK_TOKEN_TYPE_MAP["stringBlockStart"]
                )
                chunkLastCharIsStringBlockEnd = (
                    chunk[-1] in CHUNK_TOKEN_TYPE_MAP["stringBlockStart"]
                )

                if wholeChunkIsStringBlockStart and (
                    blockStartingTokenType is not TokenType.StringBlockStart
                ):
                    lineTokens.append(
                        Token(type=TokenType.StringBlockStart, text=chunk)
                    )
                    blockStartingTokenType = TokenType.StringBlockStart
                    continue
                elif wholeChunkIsStringBlockEnd:
                    lineTokens.append(Token(type=TokenType.Literal, text=tokenContent))
                    lineTokens.append(Token(type=TokenType.StringBlockEnd, text=chunk))

                    blockStartingTokenType = None
                    tokenContent = ""

                    continue

                if chunkFirstCharIsStringBlockStart:
                    blockStartingTokenType = TokenType.StringBlockStart

                    foundTokens = []
                    foundTokens.append(
                        Token(type=blockStartingTokenType, text=chunk[0])
                    )
                    foundTokens.append(Token(type=TokenType.Literal, text=chunk[1:]))
                    lineTokens = [*lineTokens, *foundTokens]

                    continue
                if chunkLastCharIsStringBlockEnd:
                    blockStartingTokenType = None

                    foundTokens = []
                    foundTokens.append(
                        Token(type=TokenType.Literal, text=(tokenContent + chunk[:-1]))
                    )
                    foundTokens.append(
                        Token(
                            type=TokenType.StringBlockEnd,
                            text=chunk[-1],
                        )
                    )
                    lineTokens = [*lineTokens, *foundTokens]

                    continue

                if blockStartingTokenType is TokenType.StringBlockStart:
                    tokenContent += chunk
                    continue

                elif isNumber(chunk):
                    lineTokens.append(Token(type=TokenType.Literal, text=chunk))
                    continue
                else:
                    lineTokens.append(Token(type=TokenType.Reference, text=chunk))
                    continue

            tokens = [*tokens, *lineTokens]
        return tokens

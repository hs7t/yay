from enum import Enum, auto

class TokenType(Enum):
    Literal = auto()
    Reference = auto()
    Command = auto()
    BlockStart = auto()
    BlockEnd = auto()
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

class BlockType(Enum):
    String = auto()
    Multiline = auto()

CHUNK_TOKEN_TYPE_MAP = {
    "commands": {
        "%": TokenType.Command,
        "!": TokenType.Command,
        "$": TokenType.Command,
    },
    "blockStart": {
        '"': TokenType.BlockStart,
        "'": TokenType.BlockStart,
        ":": TokenType.BlockStart,
    },
    "blockEnd": {
        '"': TokenType.BlockEnd,
        "'": TokenType.BlockEnd,
        ";": TokenType.BlockEnd,
    }
}

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
        blockType: None|BlockType = None
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

                if (blockType is BlockType.String):
                    lineTokens.append(
                        Token(type=TokenType.Literal, text=chunk)
                    )
                    continue

                if chunk in CHUNK_TOKEN_TYPE_MAP['blockStart']:
                    lineTokens.append(
                        Token(type=TokenType.BlockStart, text=chunk)
                    )
                    continue
                elif chunk in CHUNK_TOKEN_TYPE_MAP['blockEnd']:
                    lineTokens.append(
                        Token(type=TokenType.BlockEnd, text=chunk)
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
! print meta.title
"""

tokens: list[Token] = Tokenizer(code).getTokens()
print([[token.type, token.text] for token in tokens])
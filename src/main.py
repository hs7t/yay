from enum import Enum, auto

class VerbKind(Enum):
    Literal = auto()
    Command = auto()

class CommandType(Enum):
    Run = auto()
    ShellRun = auto()
    GlobalSet = auto()

class LiteralType(Enum):
    Integer = auto()

class BlockType(Enum):
    String = auto()
    Multiline = auto()

CHUNK_KIND_TYPE_MAP = {
    "commands": {
        "%": CommandType.GlobalSet,
        "!": CommandType.Run,
        "$": CommandType.ShellRun
    },
    "blockInitiator": {
        '"': BlockType.String,
        "'": BlockType.String        
    }
}

class Verb():
    def __init__ (self, kind: VerbKind, kindType: LiteralType|CommandType, literalValue: str|int|None = None):
        self.kind = kind
        self.kindType = kindType

        self.literalValue: str|int|None

        if (kindType == LiteralType):
            self.literalValue = literalValue
        else:
            self.literalValue = None


class Parser:
    def __init__ (self, text: str):
        self.text = text 

    def getLines(self):
        lines = self.text.splitlines()
        return [line for line in lines if len(line) != 0]

    @staticmethod
    def getVerbsOfLine(line):
        chunks = line.split()
        verbs: list[Verb] = []

        isFirstChunk = True
        isInBlock = False

        for chunk in chunks:
            verb: Verb
            if (isFirstChunk):
                if (chunk in CHUNK_KIND_TYPE_MAP["commands"]):
                    verb = Verb(VerbKind.Command, CHUNK_KIND_TYPE_MAP["commands"][chunk])
                isFirstChunk = False
                
            # verbs.append(verb)


        

code = """
% yay 0.1
! print meta.title
"""

parser = Parser(code)

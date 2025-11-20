from enum import Enum, auto

class VerbKind(Enum):
    Literal = auto()
    Command = auto()

class CommandType(Enum):
    Run = auto()
    ShellRun = auto()
    GlobalSet = auto()

class LiteralType(Enum):
    String = auto()
    Integer = auto()
    
class Verb():
    def __init__ (self, kind: VerbKind, kindType: LiteralType|CommandType, literalValue: str|int|None):
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
    def getLineVerbs(line):
        """"""
        

code = """
% yay 0.1
! print meta.title
"""

parser = Parser(code)

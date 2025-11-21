from array import array
from multiprocessing import Array
from tokenization import Token, TokenType

class Parser:
    def __init__ (self, tokens: list[Token]):
        self.tokens: list[Token] = tokens
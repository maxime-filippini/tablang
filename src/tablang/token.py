"""Tokens used in `tablang`.

This module holds the various token types and token maps used within the
`tablang` syntax.
"""

from dataclasses import dataclass
from enum import Enum


class TokenType(Enum):
    """Types of tokens included in `tablang`."""    
    GT = ">"
    LT = "<"
    EOF = "EOF"
    PIPE = "|"
    PLUS = "+"
    BANG = "!"
    MINUS = "-"
    COMMA = ","
    EQUAL = "=="
    IDENT = "IDENT"
    DIVIDE = "/"
    ASSIGN = "="
    LPAREN = "("
    RPAREN = ")"
    LCURLY = "{"
    RCURLY = "}"
    INT = "INT"
    FLOAT = "FLOAT"
    ILLEGAL = "ILLEGAL"
    ASTERISK = "*"
    GEQ = ">="
    LEQ = "<="
    NEQ = "!="
    EQ = "=="

    # Keywords
    DATE = "DATE"
    AND = "AND"
    OR = "OR"
    IF = "IF"
    ELSE = "ELSE"
    TRUE = "TRUE"
    FALSE = "FALSE"


simple_token_map = {
    "(": TokenType.LPAREN,
    ")": TokenType.RPAREN,
    "{": TokenType.LCURLY,
    "}": TokenType.RCURLY,
    "|": TokenType.PIPE,
    "*": TokenType.ASTERISK,
    "+": TokenType.PLUS,
    "!": TokenType.BANG,
    ">": TokenType.GT,
    "<": TokenType.LT,
    "=": TokenType.ASSIGN,
    ",": TokenType.COMMA,
    "-": TokenType.MINUS,
    "/": TokenType.DIVIDE,
}

double_token_map = {
    "==": TokenType.EQ,
    "!=": TokenType.NEQ,
    ">=": TokenType.GEQ,
    "<=": TokenType.LEQ,
}

keyword_map = {
    "DATE": TokenType.DATE,
    "AND": TokenType.AND,
    "OR": TokenType.OR,
    "IF": TokenType.IF,
    "ELSE": TokenType.ELSE,
    "TRUE": TokenType.TRUE,
    "FALSE": TokenType.FALSE,
}


@dataclass
class Token:
    """Data representation of a token."""    
    type_: TokenType
    literal: str

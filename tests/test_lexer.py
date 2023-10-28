
import pytest

from tablang.lexer import Lexer
from tablang.token import Token
from tablang.token import TokenType

SIMPLE_CASE = (
    "()+-{}/*",
    [
        (Token(TokenType.LPAREN, "("), 0),
        (Token(TokenType.RPAREN, ")"), 1),
        (Token(TokenType.PLUS, "+"), 2),
        (Token(TokenType.MINUS, "-"), 3),
        (Token(TokenType.LCURLY, "{"), 4),
        (Token(TokenType.RCURLY, "}"), 5),
        (Token(TokenType.DIVIDE, "/"), 6),
        (Token(TokenType.ASTERISK, "*"), 7),        
    ]
)

IDENTIFIER_CASE = (
    "test = 32",
    [
        (Token(TokenType.IDENT, "test"), 0),
        (Token(TokenType.ASSIGN, "="), 5),
        (Token(TokenType.INT, "32"), 7),
    ]
)

FLOAT_CASE = (
    "test = 28.44",
    [
        (Token(TokenType.IDENT, "test"), 0),
        (Token(TokenType.ASSIGN, "="), 5),
        (Token(TokenType.FLOAT, "28.44"), 7),
    ]
)

DOUBLE_TOKENS = (
    "A == B != C >= D <= E",
    [
        (Token(TokenType.IDENT, "A"), 0),
        (Token(TokenType.EQUAL, "=="), 2),
        (Token(TokenType.IDENT, "B"), 5),
        (Token(TokenType.NEQ, "!="), 7),
        (Token(TokenType.IDENT, "C"), 10),
        (Token(TokenType.GEQ, ">="), 12),
        (Token(TokenType.IDENT, "D"), 15),
        (Token(TokenType.LEQ, "<="), 17),
        (Token(TokenType.IDENT, "E"), 20),        
    ]
)

INT_VS_FLOAT = (
    "32 32. 32.0",
    [
        (Token(TokenType.INT, "32"), 0),
        (Token(TokenType.ILLEGAL, "32."), 3),
        (Token(TokenType.FLOAT, "32.0"), 7),
    ]
)

REALISTIC = (
    "NAV_DATE >= DATE(20221231) AND NAV_PRICE <= 200",
    [
        (Token(TokenType.IDENT, "NAV_DATE"), 0),
        (Token(TokenType.GEQ, ">="), 9),
        (Token(TokenType.DATE, "DATE"), 12),
        (Token(TokenType.LPAREN, "("), 16),
        (Token(TokenType.INT, "20221231"), 17),
        (Token(TokenType.RPAREN, ")"), 25),
        (Token(TokenType.AND, "AND"), 27),
        (Token(TokenType.IDENT, "NAV_PRICE"), 31),
        (Token(TokenType.LEQ, "<="), 41),
        (Token(TokenType.INT, "200"), 44),                
    ]
)

@pytest.mark.parametrize(
    "input,expected",
    [
        pytest.param(*SIMPLE_CASE, id="simple"),
        pytest.param(*IDENTIFIER_CASE, id="ident"),
        pytest.param(*FLOAT_CASE, id="float"),
        pytest.param(*DOUBLE_TOKENS, id="equal"),
        pytest.param(*INT_VS_FLOAT, id="int_vs_float"),
        pytest.param(*REALISTIC, id="realistic")
    ]
)
def test_lexer(input, expected):
    lex = Lexer(input)
    tokens = lex.read_input()

    assert len(tokens) == len(expected)

    for (token, pos), (expected_token, expected_pos) in zip(tokens, expected):
        assert token == expected_token
        assert pos == expected_pos



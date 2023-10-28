"""Lexer for `tablang`.

This module holds the Lexer class and utility functions for tokenizing
an input string using the definitions set in the `token` module.

"""
from tablang.token import Token
from tablang.token import TokenType
from tablang.token import double_token_map
from tablang.token import keyword_map
from tablang.token import simple_token_map

CHAR_SENTINEL = "\x00"

TypeTokenPos = tuple[Token, int]


class Lexer:
    """Lexer class for `tablang`."""

    _letterset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_"
    _numberset = "0123456789."

    def __init__(self, input: str) -> None:
        """Initialization of the lexer.

        Args:
            input (str): Input string to tokenize.
        """
        self._pos = -1
        self._read_pos = 0
        self._input = input

        self.read_char()

    def read_input(self) -> list[TypeTokenPos]:
        """Read the full input string, token by token.

        Returns:
            list[TypeTokenPos]: List of tokens and their position.
        """
        out = []
        while self._ch is not CHAR_SENTINEL:
            out.append(self.next_token())
        return out

    def read_char(self) -> None:
        """Read a single character off the input string."""
        if self._read_pos >= len(self._input):
            self._ch = CHAR_SENTINEL
        else:
            self._ch = self._input[self._read_pos]

        self._pos = self._read_pos
        self._read_pos += 1

    def peek_char(self) -> str:
        """Peek the next character off the input string.

        Returns:
            str: Character at the read position.
        """
        if self._read_pos >= len(self._input):
            return CHAR_SENTINEL
        return self._input[self._read_pos]

    def next_token(self) -> TypeTokenPos:
        """Get the next token from the input string.

        Returns:
            TypeTokenPos: Token and its position.
        """
        if self._ch is CHAR_SENTINEL:
            return (Token(TokenType.EOF, CHAR_SENTINEL), self._pos)

        out = None
        self._skip_whitespace()

        # First, we check on the simple token map
        if self._ch in simple_token_map:

            # Double tokens
            if self._ch in ("=!><"):
                next_ch = self.peek_char()
                combo = self._ch + next_ch

                if combo in double_token_map:
                    token_type = double_token_map[combo]
                    out = (Token(token_type, combo), self._pos)
                    self.read_char()

            if out is None:
                token_type = simple_token_map[self._ch]
                out = (Token(token_type, self._ch), self._pos)

        else:

            if self._ch in self._letterset:
                start_pos = self._pos
                token = self._read_identifier()
                return (token, start_pos)

            if self._ch in self._numberset:
                start_pos = self._pos
                token = self._read_number()
                return (token, start_pos)

            token = Token(TokenType.ILLEGAL, literal=self._ch)
            out = (token, self._pos)

        # Move forward
        self.read_char()
        return out

    def _skip_whitespace(self) -> None:
        """Advance through the whitespace, which is ignored in the tokenization."""
        while self._ch in (" ", "\n", "\r"):
            self.read_char()

    def _read_identifier(self) -> Token:
        """Read through the following identifier/keyword in the input string.

        Returns:
            Token: Resulting identifier/keyword token.
        """
        start_pos = self._pos

        while self._ch in self._letterset:
            self.read_char()

        lit = self._input[start_pos : self._pos]

        if lit in keyword_map:
            type_ = keyword_map[lit]
        else:
            type_ = TokenType.IDENT

        return Token(type_, literal=lit)

    def _read_number(self) -> Token:
        """Read the following number from the input string.

        Returns:
            Token: Either an INT, FLOAT or ILLEGAL token.
        """
        start_pos = self._pos
        period_count = 0

        while self._ch in self._numberset:
            if self._ch == ".":
                period_count += 1
            self.read_char()

        lit = self._input[start_pos : self._pos]

        if (lit[-1] == ".") or (lit[0] == "."):
            return Token(TokenType.ILLEGAL, lit)

        if period_count == 0:
            type_ = TokenType.INT
        elif period_count == 1:
            type_ = TokenType.FLOAT
        else:
            type_ = TokenType.ILLEGAL

        return Token(type_, lit)

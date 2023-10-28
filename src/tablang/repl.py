"""A simple REPL (not quite yet) for `tablang`.

Currently only provides the output of the lexer, i.e. no AST is being built, and
no evaluation is being performed.

"""

import argparse
from typing import Sequence

from tablang.lexer import Lexer
from tablang.token import TokenType


def main(args: Sequence[str] | None = None) -> int:
    """Entry point for the REPL.

    Args:
        args (Sequence[str] | None, optional): Command line arguments. Defaults to 
        None.

    Returns:
        int: Return code.
    """    
    parser = argparse.ArgumentParser()
    _ = parser.parse_args()

    print("Welcome to the `tablang` REPL! Start writing commands down below.")

    while True:
        try:
            input_ = input(">>> ")

            if input_.lower() in (":q", "quit()", "exit"):
                break

            lex = Lexer(input_)
            token, _ = lex.next_token()

            while token.type_ != TokenType.EOF:
                print(token)
                token, _ = lex.next_token()

        except KeyboardInterrupt:
            return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

import re

class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code
        self.tokens = []
        self.current_position = 0

    def tokenize(self):
        token_specification = [
            ("KEYWORD", r"\b(gimme|yo|say|keepdoing|nah)\b"),  # Prioritize keywords
            ("NUMBER", r"\d+"),
            ("IDENTIFIER", r"[a-zA-Z_][a-zA-Z0-9_]*"),
            ("COMPOP", r"==|!=|<=|>=|<|>"),
            ("ASSIGN", r"="),
            # ("COMPOP", r"[<>!=]=?|=="),
            ("OP", r"[+\-*/]"),
            ("SEMICOLON", r";"),
            ("LPAREN", r"\("),
            ("RPAREN", r"\)"),
            ("LBRACE", r"\{"),
            ("RBRACE", r"\}"),
            ("STRING", r'"[^"]*"'),
            ("SKIP", r"[ \t]+"),  # Skip over spaces and tabs
            ("NEWLINE", r"\n"),  # Line endings
        ]
        tok_regex = "|".join(f"(?P<{pair[0]}>{pair[1]})" for pair in token_specification)
        for match in re.finditer(tok_regex, self.source_code):
            kind = match.lastgroup
            value = match.group()
            if kind == "NUMBER":
                value = int(value)
            elif kind == "STRING":
                value = value.strip('"')
            elif kind == "SKIP" or kind == "NEWLINE":
                continue
            self.tokens.append((kind, value))
        return self.tokens
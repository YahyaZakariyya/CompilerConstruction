class Parser:
    def __init__(self, tokens):
        self.tokens = list(tokens)  # Convert to list to allow multiple iterations
        self.current_pos = 0
        self.current_token = self.tokens[0] if self.tokens else None

    def _consume(self, expected_type, expected_value=None):
        token = self.current_token
        if token is None or token[0] != expected_type or (expected_value and token[1] != expected_value):
            raise SyntaxError(f"Expected {expected_type} {expected_value}, got {token}")
        self.current_pos += 1
        self.current_token = self.tokens[self.current_pos] if self.current_pos < len(self.tokens) else None
        return token

    def _peek_token(self):
        peek_pos = self.current_pos + 1
        return self.tokens[peek_pos] if peek_pos < len(self.tokens) else None

    def parse(self):
        statements = []
        while self.current_token:
            statement = self._parse_statement()
            statements.append(statement)
            # Consume semicolon if it exists
            if self.current_token and self.current_token[0] == "SEMICOLON":
                self._consume("SEMICOLON")
        return {"type": "Program", "body": statements}

    def _parse_statement(self):
        if self.current_token[1] == "gimme":
            return self._parse_declaration()
        elif self.current_token[1] == "yo":
            return self._parse_if()
        elif self.current_token[1] == "keepdoing":
            return self._parse_while()
        elif self.current_token[0] == "IDENTIFIER" and self._peek_token()[0] == "ASSIGN":
            return self._parse_assignment()
        elif self.current_token[1] == "say":
            return self._parse_print()
        else:
            raise SyntaxError(f"Unexpected token: {self.current_token}")

    def _parse_while(self):
        self._consume("KEYWORD", "keepdoing")
        self._consume("LPAREN")
        condition = self._parse_condition()
        self._consume("RPAREN")
        self._consume("LBRACE")
        body = self._parse_block()
        self._consume("RBRACE")
        return {
            "type": "WhileLoop",
            "condition": condition,
            "body": body
        }

    def _parse_declaration(self):
        self._consume("KEYWORD", "gimme")
        identifier = self._consume("IDENTIFIER")[1]
        self._consume("ASSIGN")
        value = self._parse_expression()
        return {
            "type": "Declaration",
            "identifier": identifier,
            "value": value
        }

    def _parse_assignment(self):
        identifier = self._consume("IDENTIFIER")[1]
        self._consume("ASSIGN")
        value = self._parse_expression()
        return {
            "type": "Assignment",
            "identifier": identifier,
            "value": value
        }

    def _parse_print(self):
        self._consume("KEYWORD", "say")
        value = self._consume("STRING")[1]
        return {
            "type": "Print",
            "value": value
        }

    def _parse_condition(self):
        left = self._parse_expression()
        operator = self._consume("COMPOP")[1]
        right = self._parse_expression()
        return {
            "type": "Condition",
            "left": left,
            "operator": operator,
            "right": right
        }

    def _parse_block(self):
        statements = []
        while self.current_token and self.current_token[1] != "}":
            statement = self._parse_statement()
            statements.append(statement)
            # Consume semicolon if it exists
            if self.current_token and self.current_token[0] == "SEMICOLON":
                self._consume("SEMICOLON")
        return statements

    # def _parse_expression(self):
    #     token = self.current_token
    #     if token[0] == "NUMBER":
    #         self._consume("NUMBER")
    #         return {"type": "Number", "value": int(token[1])}
    #     elif token[0] == "IDENTIFIER":
    #         self._consume("IDENTIFIER")
    #         return {"type": "Variable", "name": token[1]}
    #     else:
    #         raise SyntaxError(f"Unexpected token in expression: {token}")
        
    def _parse_if(self):
        self._consume("KEYWORD", "yo")
        self._consume("LPAREN")
        condition = self._parse_condition()
        self._consume("RPAREN")
        self._consume("LBRACE")
        if_body = self._parse_block()
        self._consume("RBRACE")
        
        else_body = []
        if self.current_token and self.current_token[1] == "nah":
            self._consume("KEYWORD", "nah")
            self._consume("LBRACE")
            else_body = self._parse_block()
            self._consume("RBRACE")
            
        return {
            "type": "IfStatement",
            "condition": condition,
            "if_body": if_body,
            "else_body": else_body
        }

    def _parse_expression(self):
        # # First check if it's a simple term (number, string, or variable)
        # if self.current_token[0] in ["NUMBER", "STRING", "IDENTIFIER"]:
        #     token = self.current_token
        #     self._consume(token[0])
        #     if token[0] == "NUMBER":
        #         return {"type": "Number", "value": int(token[1])}
        #     elif token[0] == "STRING":
        #         return {"type": "String", "value": token[1]}
        #     else:
        #         return {"type": "Variable", "name": token[1]}
        
        # If not, parse as a potentially complex expression
        left = self._parse_term()
        
        while self.current_token and self.current_token[0] == "OP":
            operator = self._consume("OP")[1]
            right = self._parse_term()
            left = {
                "type": "Operation",
                "operator": operator,
                "left": left,
                "right": right
            }
        
        return left
    
    def _parse_term(self):
        token = self.current_token
        if token[0] == "NUMBER":
            self._consume("NUMBER")
            return {"type": "Number", "value": int(token[1])}
        elif token[0] == "STRING":
            self._consume("STRING")
            return {"type": "String", "value": token[1]}
        elif token[0] == "IDENTIFIER":
            self._consume("IDENTIFIER")
            return {"type": "Variable", "name": token[1]}
        elif token[0] == "LPAREN":
            self._consume("LPAREN")
            expr = self._parse_expression()
            self._consume("RPAREN")
            return expr
        else:
            raise SyntaxError(f"Unexpected token in expression: {token}")
        
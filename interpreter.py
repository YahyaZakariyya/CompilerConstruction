from symbol_table import SymbolTable

class Interpreter:
    def __init__(self, parse_tree):
        self.parse_tree = parse_tree
        self.symbol_table = SymbolTable()
        self.output = []

    def execute(self):
        for statement in self.parse_tree["body"]:
            self._execute_statement(statement)
        return self.output

    def _evaluate_condition(self, condition):
        left = self._evaluate_expression(condition["left"])
        right = self._evaluate_expression(condition["right"])
        operator = condition["operator"]

        # Handle comparison between strings and numbers
        if isinstance(left, str) or isinstance(right, str):
            # For strings, only allow == and != operators
            if operator == "==":
                return str(left) == str(right)
            elif operator == "!=":
                return str(left) != str(right)
            else:
                raise ValueError("String comparisons only support == and != operators")
        else:
            # Numeric comparisons
            if operator == "<":
                return left < right
            elif operator == ">":
                return left > right
            elif operator == "==":
                return left == right
            elif operator == "!=":
                return left != right
            elif operator == "<=":
                return left <= right
            elif operator == ">=":
                return left >= right
            else:
                raise ValueError(f"Unknown operator: {operator}")
    
    def _execute_statement(self, statement):
        if statement["type"] == "Declaration":
            value = self._evaluate_expression(statement["value"])
            self.symbol_table.declare(statement["identifier"], value)
        elif statement["type"] == "Assignment":
            value = self._evaluate_expression(statement["value"])
            self.symbol_table.assign(statement["identifier"], value)
        elif statement["type"] == "IfStatement":
            condition = self._evaluate_condition(statement["condition"])
            if condition:
                for stmt in statement["if_body"]:
                    self._execute_statement(stmt)
            elif statement["else_body"]:
                for stmt in statement["else_body"]:
                    self._execute_statement(stmt)
        elif statement["type"] == "WhileLoop":
            while self._evaluate_condition(statement["condition"]):
                for stmt in statement["body"]:
                    self._execute_statement(stmt)
        elif statement["type"] == "Print":
            value = statement["value"]
            print(value)  # Print to console
            self.output.append(value)
        else:
            raise ValueError(f"Unknown statement type: {statement['type']}")

    def _evaluate_expression(self, expression):
        if expression["type"] == "Number":
            return expression["value"]
        elif expression["type"] == "String":
            return expression["value"]
        elif expression["type"] == "Variable":
            return self.symbol_table.lookup(expression["name"])
        elif expression["type"] == "Operation":
            left = self._evaluate_expression(expression["left"])
            right = self._evaluate_expression(expression["right"])
            
            # Check if either operand is a string for string concatenation
            if isinstance(left, str) or isinstance(right, str):
                if expression["operator"] == "+":
                    return str(left) + str(right)
                else:
                    raise ValueError("Only + operator is supported for strings")
            
            # Numeric operations
            if not (isinstance(left, (int, float)) and isinstance(right, (int, float))):
                raise ValueError("Arithmetic operations only support numbers")
                
            if expression["operator"] == "+":
                return left + right
            elif expression["operator"] == "-":
                return left - right
            elif expression["operator"] == "*":
                return left * right
            elif expression["operator"] == "/":
                if right == 0:
                    raise ValueError("Division by zero")
                return left // right  # Using integer division
        else:
            raise ValueError(f"Unknown expression type: {expression['type']}")
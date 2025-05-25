from lexer import Lexer, TokenType
from ast_nodes import (
    Assignment, Variable, BinaryOp, Number, Print, Float, String, Boolean,
    UnaryOp, IfStatement, WhileLoop, ForLoop, RangeCall, FunctionDef, FunctionCall, Return, 
    List, ListAccess, ListAssignment, LenCall, Program
)

class Parser:
    """Parses tokens into an Abstract Syntax Tree (AST)."""
    
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0
        self.current_token = self.tokens[self.current_token_index]

    def eat(self, token_type):
        """Consume a token if it matches the expected type."""
        if self.current_token.type == token_type:
            self.current_token_index += 1
            if self.current_token_index < len(self.tokens):
                self.current_token = self.tokens[self.current_token_index]
            else:
                self.current_token = None
        else:
            raise SyntaxError(f"Expected token type {token_type}, but got {self.current_token.type} at line {self.current_token.line}, column {self.current_token.column}")

    def parse_literal(self):
        """Parse a literal value (number, float, string, boolean)."""
        if self.current_token.type == TokenType.NUMBER:
            token = self.current_token
            self.eat(TokenType.NUMBER)
            return Number(token.value)
        elif self.current_token.type == TokenType.FLOAT:
            token = self.current_token
            self.eat(TokenType.FLOAT)
            return Float(token.value)
        elif self.current_token.type == TokenType.STRING:
            token = self.current_token
            self.eat(TokenType.STRING)
            return String(token.value)
        elif self.current_token.type in (TokenType.TRUE, TokenType.FALSE):
            token = self.current_token
            self.eat(token.type)
            return Boolean(token.value)
        else:
            raise SyntaxError(f"Unexpected token: {self.current_token}")

    def parse_variable(self):
        """Parse a variable and return a Variable AST node."""
        token = self.current_token
        self.eat(TokenType.IDENTIFIER)
        return Variable(token.value)

    def parse_expression(self):
        """Parse expressions with proper operator precedence."""
        print(f"Parsing expression at token: {self.current_token}")
        # Handle expressions that start with operators
        if self.current_token and self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            operator = self.current_token.value
            self.eat(self.current_token.type)
            operand = self.parse_expression()
            return UnaryOp(operator, operand)
        expr = self.parse_logical()
        return expr

    def parse_comparison(self):
        """Parse comparison operators."""
        print(f"Parsing comparison at token: {self.current_token}")
        left = self.parse_term()

        while self.current_token and self.current_token.type in (
            TokenType.GREATER, TokenType.LESS, TokenType.GREATER_EQUALS,
            TokenType.LESS_EQUALS, TokenType.EQUALS_EQUALS, TokenType.NOT_EQUALS
        ):
            operator = self.current_token.value
            self.eat(self.current_token.type)
            right = self.parse_term()
            left = BinaryOp(left, operator, right)

        return left

    def parse_term(self):
        """Parse addition and subtraction."""
        print(f"Parsing term at token: {self.current_token}")
        left = self.parse_factor()

        while self.current_token and self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            operator = self.current_token.value
            print(f"Found operator {operator} at token: {self.current_token}")
            self.eat(self.current_token.type)
            right = self.parse_factor()
            
            # Handle string concatenation
            if operator == '+':
                # If either operand is a string or str() call, treat as string concatenation
                if isinstance(left, String) or isinstance(right, String) or \
                   (isinstance(left, FunctionCall) and left.name == 'str') or \
                   (isinstance(right, FunctionCall) and right.name == 'str'):
                    # Convert non-string operands to strings
                    if not isinstance(left, String) and not (isinstance(left, FunctionCall) and left.name == 'str'):
                        left = FunctionCall('str', [left])
                    if not isinstance(right, String) and not (isinstance(right, FunctionCall) and right.name == 'str'):
                        right = FunctionCall('str', [right])
            
            left = BinaryOp(left, operator, right)

        return left

    def parse_factor(self):
        """Parse multiplication and division."""
        print(f"Parsing factor at token: {self.current_token}")
        left = self.parse_primary()

        while self.current_token and self.current_token.type in (TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO):
            operator = self.current_token.value
            self.eat(self.current_token.type)
            right = self.parse_primary()
            left = BinaryOp(left, operator, right)

        return left

    def parse_primary(self):
        """Parse a primary expression."""
        print(f"parse_primary: current token = {self.current_token}")
        if not self.current_token:
            return None
            
        token = self.current_token

        if token.type == TokenType.NUMBER:
            self.eat(TokenType.NUMBER)
            return Number(token.value)
        elif token.type == TokenType.FLOAT:
            self.eat(TokenType.FLOAT)
            return Float(token.value)
        elif token.type == TokenType.STRING:
            self.eat(TokenType.STRING)
            return String(token.value)
        elif token.type == TokenType.TRUE:
            self.eat(TokenType.TRUE)
            return Boolean(True)
        elif token.type == TokenType.FALSE:
            self.eat(TokenType.FALSE)
            return Boolean(False)
        elif token.type == TokenType.IDENTIFIER:
            name = token.value
            self.eat(TokenType.IDENTIFIER)
            
            # Check for function call
            if self.current_token and self.current_token.type == TokenType.LPAREN:
                return self.parse_function_call(name)
            
            # Check for list access
            elif self.current_token and self.current_token.type == TokenType.LBRACKET:
                self.eat(TokenType.LBRACKET)
                index = self.parse_expression()
                self.eat(TokenType.RBRACKET)
                return ListAccess(Variable(name), index)
            
            return Variable(name)
        elif token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            expr = self.parse_expression()
            self.eat(TokenType.RPAREN)
            return expr
        elif token.type == TokenType.LBRACKET:
            self.eat(TokenType.LBRACKET)
            elements = []
            if self.current_token and self.current_token.type != TokenType.RBRACKET:
                while True:
                    elements.append(self.parse_expression())
                    if not self.current_token or self.current_token.type == TokenType.RBRACKET:
                        break
                    self.eat(TokenType.COMMA)
            self.eat(TokenType.RBRACKET)
            return List(elements)
        elif token.type in (TokenType.PLUS, TokenType.MINUS):
            # Handle unary operators
            operator = token.value
            self.eat(token.type)
            operand = self.parse_primary()
            return UnaryOp(operator, operand)
        else:
            # If we encounter an operator here, it's likely part of a larger expression
            # Let the caller handle it
            return None

    def parse_function_call(self, name):
        """Parse a function call with its arguments."""
        self.eat(TokenType.LPAREN)
        args = []
        if self.current_token and self.current_token.type != TokenType.RPAREN:
            args.append(self.parse_expression())
            while self.current_token and self.current_token.type == TokenType.COMMA:
                self.eat(TokenType.COMMA)
                args.append(self.parse_expression())
        self.eat(TokenType.RPAREN)
        return FunctionCall(name, args)

    def parse_multiple_assignment(self):
        """Parse multiple assignments like 'a, b = c, d' or 'arr[i], arr[j] = arr[j], arr[i]'."""
        targets = []
        values = []
        
        # Parse targets
        while True:
            if self.current_token.type == TokenType.IDENTIFIER:
                var_name = self.current_token.value
                self.eat(TokenType.IDENTIFIER)
                
                # Check for list access
                if self.current_token.type == TokenType.LBRACKET:
                    self.eat(TokenType.LBRACKET)
                    index = self.parse_expression()
                    self.eat(TokenType.RBRACKET)
                    targets.append(ListAccess(Variable(var_name), index))
                else:
                    targets.append(Variable(var_name))
            
            if self.current_token.type != TokenType.COMMA:
                break
            self.eat(TokenType.COMMA)
        
        # Parse equals sign
        self.eat(TokenType.EQUALS)
        
        # Parse values
        while True:
            if self.current_token.type == TokenType.IDENTIFIER:
                var_name = self.current_token.value
                self.eat(TokenType.IDENTIFIER)
                
                # Check for list access
                if self.current_token.type == TokenType.LBRACKET:
                    self.eat(TokenType.LBRACKET)
                    index = self.parse_expression()
                    self.eat(TokenType.RBRACKET)
                    values.append(ListAccess(Variable(var_name), index))
                else:
                    values.append(Variable(var_name))
            else:
                values.append(self.parse_expression())
            
            if self.current_token.type != TokenType.COMMA:
                break
            self.eat(TokenType.COMMA)
        
        # Create assignments
        statements = []
        for target, value in zip(targets, values):
            if isinstance(target, ListAccess):
                statements.append(ListAssignment(target.list_expr, target.index, value))
            else:
                statements.append(Assignment(target, value))
        
        return statements

    def parse_statement(self):
        """Parse a single statement."""
        if self.current_token.type == TokenType.IF:
            return self.parse_if()
        elif self.current_token.type == TokenType.WHILE:
            return self.parse_while()
        elif self.current_token.type == TokenType.FOR:
            return self.parse_for()
        elif self.current_token.type == TokenType.DEF:
            return self.parse_function_def()
        elif self.current_token.type == TokenType.RETURN:
            return self.parse_return()
        elif self.current_token.type == TokenType.PRINT:
            return self.parse_print()
        elif self.current_token.type == TokenType.IDENTIFIER:
            var_name = self.current_token.value
            self.eat(TokenType.IDENTIFIER)
            
            # Check for function call
            if self.current_token.type == TokenType.LPAREN:
                return self.parse_function_call(var_name)
            
            # Check for list assignment
            if self.current_token.type == TokenType.LBRACKET:
                self.eat(TokenType.LBRACKET)
                index = self.parse_expression()
                self.eat(TokenType.RBRACKET)
                
                # Check for tuple unpacking
                if self.current_token.type == TokenType.COMMA:
                    # Handle tuple unpacking assignment
                    return self.parse_multiple_assignment()
                
                # Regular list assignment
                self.eat(TokenType.EQUALS)
                value = self.parse_expression()
                return ListAssignment(Variable(var_name), index, value)
            
            # Check for augmented assignment
            if self.current_token.type in (TokenType.PLUS_EQUALS, TokenType.MINUS_EQUALS, 
                                         TokenType.MULTIPLY_EQUALS, TokenType.DIVIDE_EQUALS,
                                         TokenType.MODULO_EQUALS):
                operator = self.current_token.value
                self.eat(self.current_token.type)
                value = self.parse_expression()
                # Convert augmented assignment to regular assignment with binary operation
                op_map = {
                    '+=': '+',
                    '-=': '-',
                    '*=': '*',
                    '/=': '/',
                    '%=': '%'
                }
                binary_op = BinaryOp(Variable(var_name), op_map[operator], value)
                return Assignment(Variable(var_name), binary_op)
            
            # Regular assignment
            if self.current_token.type == TokenType.EQUALS:
                self.eat(TokenType.EQUALS)
                expression = self.parse_expression()
                return Assignment(Variable(var_name), expression)
            else:
                # If no equals sign, treat as an expression
                return Variable(var_name)
        elif self.current_token.type in (TokenType.PLUS, TokenType.MINUS, TokenType.STRING, TokenType.NUMBER, TokenType.FLOAT, TokenType.TRUE, TokenType.FALSE):
            # Handle expressions that start with operators or literals
            return self.parse_expression()
        else:
            raise SyntaxError(f"Invalid statement: {self.current_token}")

    def parse_if(self):
        """Parse an if statement."""
        self.eat(TokenType.IF)
        condition = self.parse_logical()
        self.eat(TokenType.COLON)
        body = self.parse_block()
        
        else_body = None
        if self.current_token.type == TokenType.ELSE:
            self.eat(TokenType.ELSE)
            self.eat(TokenType.COLON)
            else_body = self.parse_block()
        
        return IfStatement(condition, body, else_body)

    def parse_while(self):
        """Parse a while loop."""
        self.eat(TokenType.WHILE)
        condition = self.parse_logical()
        self.eat(TokenType.COLON)
        body = self.parse_block()
        return WhileLoop(condition, body)

    def parse_for(self):
        """Parse a for loop."""
        self.eat(TokenType.FOR)
        var_name = self.current_token.value
        self.eat(TokenType.IDENTIFIER)
        self.eat(TokenType.IN)
        
        # Handle range() function
        if self.current_token.type == TokenType.RANGE:
            self.eat(TokenType.RANGE)
            self.eat(TokenType.LPAREN)
            
            # Parse start
            start = self.parse_expression()
            
            # Check for end and step parameters
            if self.current_token.type == TokenType.COMMA:
                self.eat(TokenType.COMMA)
                end = self.parse_expression()
                
                # Check for step parameter
                if self.current_token.type == TokenType.COMMA:
                    self.eat(TokenType.COMMA)
                    step = self.parse_expression()
                else:
                    step = None
            else:
                end = start
                start = Number(0)
                step = None
            
            self.eat(TokenType.RPAREN)
            iterable = RangeCall(start, end, step)
        else:
            iterable = self.parse_expression()
        
        self.eat(TokenType.COLON)
        body = self.parse_block()
        
        return ForLoop(var_name, iterable, body)

    def parse_function_def(self):
        """Parse a function definition."""
        self.eat(TokenType.DEF)
        name = self.current_token.value
        self.eat(TokenType.IDENTIFIER)
        self.eat(TokenType.LPAREN)
        
        params = []
        if self.current_token.type != TokenType.RPAREN:
            params.append(self.current_token.value)
            self.eat(TokenType.IDENTIFIER)
            while self.current_token.type == TokenType.COMMA:
                self.eat(TokenType.COMMA)
                params.append(self.current_token.value)
                self.eat(TokenType.IDENTIFIER)
        
        self.eat(TokenType.RPAREN)
        self.eat(TokenType.COLON)
        body = self.parse_block()
        return FunctionDef(name, params, body)

    def parse_return(self):
        """Parse a return statement."""
        self.eat(TokenType.RETURN)
        expression = self.parse_expression()
        return Return(expression)

    def parse_print(self):
        """Parse a print statement."""
        self.eat(TokenType.PRINT)
        self.eat(TokenType.LPAREN)
        expressions = []
        
        # Parse first expression
        expressions.append(self.parse_expression())
        
        # Parse additional expressions separated by commas
        while self.current_token.type == TokenType.COMMA:
            self.eat(TokenType.COMMA)
            expressions.append(self.parse_expression())
        
        self.eat(TokenType.RPAREN)
        return Print(expressions)

    def parse_block(self):
        """Parse a block of statements."""
        statements = []
        while self.current_token and self.current_token.type not in (TokenType.EOF, TokenType.ELSE):
            # Only parse statements, not function definitions, in blocks
            if self.current_token.type == TokenType.DEF:
                # Skip nested function definitions (treat as top-level only)
                break
            statements.append(self.parse_statement())
        return statements

    def parse_logical(self):
        """Parse logical operators (and, or)."""
        print(f"Parsing logical at token: {self.current_token}")
        left = self.parse_comparison()

        while self.current_token and self.current_token.type in (TokenType.AND, TokenType.OR):
            operator = self.current_token.value
            self.eat(self.current_token.type)
            right = self.parse_comparison()
            left = BinaryOp(left, operator, right)

        return left

    def parse(self):
        """Parse multiple statements into an AST list."""
        statements = []
        while self.current_token and self.current_token.type != TokenType.EOF:
            if self.current_token.type == TokenType.DEF:
                statements.append(self.parse_function_def())
            else:
                statements.append(self.parse_statement())
        return Program(statements)

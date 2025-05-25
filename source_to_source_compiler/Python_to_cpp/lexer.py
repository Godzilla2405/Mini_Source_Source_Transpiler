import re
from tokens import TokenType

class Token:
    """Represents a single token."""
    def __init__(self, type_, value, line=None, column=None):
        self.type = type_
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Token({self.type}, {self.value}, line={self.line}, col={self.column})"

class Lexer:
    """Converts Python code into tokens."""
    
    def __init__(self, source_code):
        self.source_code = source_code
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens = []
    
    def tokenize(self):
        """Main function to generate tokens from source code."""
        token_specification = [
            # Keywords
            ('PRINT', r'\bprint\b', TokenType.PRINT),
            ('IF', r'\bif\b', TokenType.IF),
            ('ELSE', r'\belse\b', TokenType.ELSE),
            ('WHILE', r'\bwhile\b', TokenType.WHILE),
            ('FOR', r'\bfor\b', TokenType.FOR),
            ('IN', r'\bin\b', TokenType.IN),
            ('RANGE', r'\brange\b', TokenType.RANGE),
            ('DEF', r'\bdef\b', TokenType.DEF),
            ('RETURN', r'\breturn\b', TokenType.RETURN),
            ('TRUE', r'\bTrue\b', TokenType.TRUE),
            ('FALSE', r'\bFalse\b', TokenType.FALSE),
            ('AND', r'\band\b', TokenType.AND),
            ('OR', r'\bor\b', TokenType.OR),
            ('NOT', r'\bnot\b', TokenType.NOT),
            
            # Identifiers and literals
            ('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*', TokenType.IDENTIFIER),
            ('FLOAT', r'\d*\.\d+', TokenType.FLOAT),
            ('NUMBER', r'\d+', TokenType.NUMBER),
            ('STRING', r'"[^"\\]*(\\.[^"\\]*)*"|\'[^\'\\]*(\\.[^\'\\]*)*\'', TokenType.STRING),
            
            # Operators
            ('PLUS_EQUALS', r'\+=', TokenType.PLUS_EQUALS),
            ('MINUS_EQUALS', r'-=', TokenType.MINUS_EQUALS),
            ('MULTIPLY_EQUALS', r'\*=', TokenType.MULTIPLY_EQUALS),
            ('DIVIDE_EQUALS', r'/=', TokenType.DIVIDE_EQUALS),
            ('MODULO_EQUALS', r'%=', TokenType.MODULO_EQUALS),
            ('EQUALS_EQUALS', r'==', TokenType.EQUALS_EQUALS),
            ('NOT_EQUALS', r'!=', TokenType.NOT_EQUALS),
            ('GREATER_EQUALS', r'>=', TokenType.GREATER_EQUALS),
            ('LESS_EQUALS', r'<=', TokenType.LESS_EQUALS),
            ('EQUALS', r'=', TokenType.EQUALS),
            ('PLUS', r'\+', TokenType.PLUS),
            ('MINUS', r'-', TokenType.MINUS),
            ('MULTIPLY', r'\*', TokenType.MULTIPLY),
            ('DIVIDE', r'/', TokenType.DIVIDE),
            ('MODULO', r'%', TokenType.MODULO),
            ('GREATER', r'>', TokenType.GREATER),
            ('LESS', r'<', TokenType.LESS),
            
            # Delimiters
            ('LPAREN', r'\(', TokenType.LPAREN),
            ('RPAREN', r'\)', TokenType.RPAREN),
            ('LBRACE', r'\{', TokenType.LBRACE),
            ('RBRACE', r'\}', TokenType.RBRACE),
            ('LBRACKET', r'\[', TokenType.LBRACKET),
            ('RBRACKET', r'\]', TokenType.RBRACKET),
            ('COMMA', r',', TokenType.COMMA),
            ('COLON', r':', TokenType.COLON),
            ('SEMICOLON', r';', TokenType.SEMICOLON),
            
            # Comments
            ('COMMENT', r'#.*', TokenType.COMMENT),
            
            # Skip whitespace
            ('SKIP', r'[ \t]+', None),
            ('NEWLINE', r'\n', None),
        ]

        token_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern, _ in token_specification)
        token_types = {name: type_ for name, _, type_ in token_specification}
        
        for match in re.finditer(token_regex, self.source_code):
            token_type = match.lastgroup
            token_value = match.group(token_type)
            start_pos = match.start()
            
            # Skip whitespace and comments
            if token_type in ('SKIP', 'COMMENT'):
                self.column += len(token_value)
                continue
                
            # Handle newlines
            if token_type == 'NEWLINE':
                self.line += 1
                self.column = 1
                continue
            
            # Convert token values to appropriate types
            if token_type == 'NUMBER':
                token_value = int(token_value)
            elif token_type == 'FLOAT':
                token_value = float(token_value)
            elif token_type == 'STRING':
                token_value = token_value[1:-1]  # Remove quotes
            elif token_type == 'TRUE':
                token_value = True
            elif token_type == 'FALSE':
                token_value = False
            elif token_type in ('PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE', 'MODULO', 
                              'EQUALS_EQUALS', 'NOT_EQUALS', 'GREATER_EQUALS', 
                              'LESS_EQUALS', 'GREATER', 'LESS', 'EQUALS'):
                token_value = token_value  # Keep the operator symbol as the value
            elif token_type == 'AND':
                token_value = 'and'
            elif token_type == 'OR':
                token_value = 'or'
            elif token_type == 'NOT':
                token_value = 'not'
            
            # Create token with original string length for column tracking
            self.tokens.append(Token(token_types[token_type], token_value, self.line, self.column))
            self.column += len(match.group(token_type))

        self.tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        return self.tokens

from enum import Enum

class TokenType(Enum):
    # Keywords
    PRINT = 'PRINT'
    IF = 'IF'
    ELSE = 'ELSE'
    WHILE = 'WHILE'
    FOR = 'FOR'
    IN = 'IN'
    RANGE = 'RANGE'
    DEF = 'DEF'
    RETURN = 'RETURN'
    TRUE = 'TRUE'
    FALSE = 'FALSE'
    
    # Identifiers and literals
    IDENTIFIER = 'IDENTIFIER'
    NUMBER = 'NUMBER'
    FLOAT = 'FLOAT'
    STRING = 'STRING'
    
    # Operators
    EQUALS = 'EQUALS'
    PLUS_EQUALS = 'PLUS_EQUALS'
    MINUS_EQUALS = 'MINUS_EQUALS'
    MULTIPLY_EQUALS = 'MULTIPLY_EQUALS'
    DIVIDE_EQUALS = 'DIVIDE_EQUALS'
    MODULO_EQUALS = 'MODULO_EQUALS'
    PLUS = 'PLUS'
    MINUS = 'MINUS'
    MULTIPLY = 'MULTIPLY'
    DIVIDE = 'DIVIDE'
    MODULO = 'MODULO'
    GREATER = 'GREATER'
    LESS = 'LESS'
    GREATER_EQUALS = 'GREATER_EQUALS'
    LESS_EQUALS = 'LESS_EQUALS'
    EQUALS_EQUALS = 'EQUALS_EQUALS'
    NOT_EQUALS = 'NOT_EQUALS'
    AND = 'AND'
    OR = 'OR'
    NOT = 'NOT'
    
    # Delimiters
    LPAREN = 'LPAREN'
    RPAREN = 'RPAREN'
    LBRACE = 'LBRACE'
    RBRACE = 'RBRACE'
    LBRACKET = 'LBRACKET'
    RBRACKET = 'RBRACKET'
    COMMA = 'COMMA'
    COLON = 'COLON'
    SEMICOLON = 'SEMICOLON'
    
    # Special
    EOF = 'EOF'
    COMMENT = 'COMMENT'

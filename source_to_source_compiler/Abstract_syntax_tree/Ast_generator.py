class Node:
    """Base class for all AST nodes."""
    pass

class Number(Node):
    def __init__(self, value):
        self.value = value
    
    def __repr__(self):
        return f"Number({self.value})"

class Variable(Node):
    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return f"Variable({self.name})"

class BinaryOp(Node):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right
    
    def __repr__(self):
        return f"BinaryOp({self.left} {self.operator} {self.right})"

class Assignment(Node):
    def __init__(self, variable, expression):
        self.variable = variable
        self.expression = expression
    
    def __repr__(self):
        return f"Assignment({self.variable} = {self.expression})"

class Print(Node):
    def __init__(self, expression):
        self.expression = expression
    
    def __repr__(self):
        return f"Print({self.expression})"

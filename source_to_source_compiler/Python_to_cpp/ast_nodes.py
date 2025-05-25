class Node:
    """Base class for all AST nodes."""
    pass

class Expression(Node):
    """Base class for all expressions."""
    pass

class Statement(Node):
    """Base class for all statements."""
    pass

class Program(Node):
    """Represents the entire program."""
    def __init__(self, statements):
        self.statements = statements

    def __repr__(self):
        return f"Program({self.statements})"

class Number(Expression):
    """Represents a number literal."""
    def __init__(self, value):
        self.value = value
    
    def __repr__(self):
        return f"Number({self.value})"

class Float(Expression):
    def __init__(self, value):
        self.value = value

class String(Expression):
    """Represents a string literal."""
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"String({self.value})"

class Boolean(Expression):
    """Represents a boolean literal."""
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Boolean({self.value})"

class Variable(Expression):
    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return f"Variable({self.name})"

class BinaryOp(Expression):
    """Represents a binary operation."""
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right
    
    def __repr__(self):
        return f"BinaryOp({self.left}, {self.op}, {self.right})"

class UnaryOp(Expression):
    """Represents a unary operation (e.g., +x, -x)."""
    def __init__(self, operator, operand):
        self.operator = operator
        self.operand = operand

    def __repr__(self):
        return f"UnaryOp({self.operator}, {self.operand})"

class Assignment(Statement):
    """Represents a variable assignment."""
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        return f"Assignment({self.name}, {self.value})"

class Print(Node):
    """Represents a print statement."""
    def __init__(self, expressions):
        self.expressions = expressions
    
    def __repr__(self):
        return f"Print({', '.join(str(expr) for expr in self.expressions)})"

# Future extensions (for handling complex programs)
class IfStatement(Statement):
    """Represents an if statement."""
    def __init__(self, condition, body, else_body=None):
        self.condition = condition
        self.body = body
        self.else_body = else_body

    def __repr__(self):
        return f"IfStatement({self.condition}, {self.body}, {self.else_body})"

class WhileLoop(Statement):
    """Represents a while loop."""
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return f"WhileLoop({self.condition}, {self.body})"

class ForLoop(Statement):
    """Represents a for loop."""
    def __init__(self, var_name, iterable, body):
        self.var_name = var_name
        self.iterable = iterable
        self.body = body

    def __repr__(self):
        return f"ForLoop({self.var_name}, {self.iterable}, {self.body})"

class RangeCall(Expression):
    """Represents a range() function call."""
    def __init__(self, start, end=None, step=None):
        self.start = start
        self.end = end
        self.step = step

    def __repr__(self):
        return f"RangeCall({self.start}, {self.end}, {self.step})"

class FunctionDef(Statement):
    """Represents a function definition."""
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

    def __repr__(self):
        return f"FunctionDef({self.name}, {self.params}, {self.body})"

class FunctionCall(Expression):
    """Represents a function call."""
    def __init__(self, name, args):
        self.name = name
        self.args = args

    def __repr__(self):
        return f"FunctionCall({self.name}, {self.args})"

class Return(Statement):
    """Represents a return statement."""
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Return({self.value})"

class List(Expression):
    def __init__(self, elements):
        self.elements = elements

class ListAccess(Expression):
    """Represents a list access."""
    def __init__(self, list_expr, index):
        self.list_expr = list_expr
        self.index = index

    def __repr__(self):
        return f"ListAccess({self.list_expr}, {self.index})"

class ListAssignment(Statement):
    """Represents a list assignment."""
    def __init__(self, list_expr, index, value):
        self.list_expr = list_expr
        self.index = index
        self.value = value

    def __repr__(self):
        return f"ListAssignment({self.list_expr}, {self.index}, {self.value})"

class LenCall(Expression):
    """Represents a len() function call."""
    def __init__(self, arg):
        self.arg = arg

    def __repr__(self):
        return f"LenCall({self.arg})"

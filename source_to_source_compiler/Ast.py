import ast
code = """
def add(x, y):
    return x + y
"""
tree = ast.parse(code)
print(ast.dump(tree, indent=4))

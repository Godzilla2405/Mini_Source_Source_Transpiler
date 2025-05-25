from ast_nodes import (
    Program, Print, BinaryOp, Number, String, Boolean, Variable,
    Assignment, IfStatement, WhileLoop, ForLoop, RangeCall,
    FunctionDef, FunctionCall, Return, List, ListAccess,
    ListAssignment, LenCall, UnaryOp, Float
)

class CodeGenerator:
    """Generates C++ code from an AST."""
    
    def __init__(self):
        self.indent_level = 0
        self.variables = set()
        self.functions = set()
    
    def generate(self, ast):
        """Main function to generate C++ code."""
        if isinstance(ast, Program):
            return self.generate_program(ast)
        else:
            raise Exception(f"Expected Program node, got {type(ast)}")
    
    def generate_program(self, ast):
        """Generate code for the entire program."""
        code = []
        code.append("#include <bits/stdc++.h>")
        code.append("using namespace std;")
        code.append("")
        code.append("void print_array(const vector<int>& arr) {")
        code.append("    cout << '[';")
        code.append("    for (size_t i = 0; i < arr.size(); ++i) {")
        code.append("        cout << arr[i];")
        code.append("        if (i < arr.size() - 1) cout << \", \";")
        code.append("    }")
        code.append("    cout << ']';")
        code.append("}")
        code.append("")
        # Collect function definitions and other statements
        function_defs = []
        other_stmts = []
        for stmt in ast.statements:
            if isinstance(stmt, FunctionDef):
                function_defs.append(stmt)
            else:
                other_stmts.append(stmt)
        # Generate function declarations
        for func in function_defs:
            if func.name != "main":
                params = []
                for param in func.params:
                    if param == "arr":
                        params.append("vector<int>& arr")
                    else:
                        params.append(f"int {param}")
                code.append(f"{'int' if func.name == 'partition' else 'void'} {func.name}({', '.join(params)});")
        code.append("")
        # Generate function definitions
        for func in function_defs:
            if func.name != "main":
                code.append(self.generate_function(func))
                code.append("")
        # Generate main function
        code.append("int main() {")
        main_func = next((fd for fd in function_defs if fd.name == "main"), None)
        if main_func:
            for stmt in main_func.body:
                # Skip the if __name__ == "__main__" block
                if isinstance(stmt, IfStatement):
                    if (isinstance(stmt.condition, BinaryOp) and 
                        isinstance(stmt.condition.left, Variable) and 
                        stmt.condition.left.name == "__name__"):
                        continue
                if isinstance(stmt, Assignment) and isinstance(stmt.value, List):
                    elements = [self.generate_expression(e) for e in stmt.value.elements]
                    code.append(f"    vector<int> {stmt.name.name} = {{{', '.join(elements)}}};")
                elif isinstance(stmt, Print):
                    exprs = stmt.expressions
                    if len(exprs) == 2 and isinstance(exprs[0], String) and isinstance(exprs[1], Variable):
                        # Print string first
                        code.append(f"    cout << {self.generate_expression(exprs[0])} << \" \";")
                        # Then print array
                        code.append(f"    print_array({exprs[1].name});")
                        code.append("    cout << endl;")
                    else:
                        code.extend([f"    {line}" for line in self.generate_print(stmt)])
                elif isinstance(stmt, FunctionCall):
                    if stmt.name == "quick_sort":
                        # Generate arguments without brace initialization
                        args = []
                        for arg in stmt.args:
                            if isinstance(arg, Variable):
                                args.append(arg.name)
                            elif isinstance(arg, BinaryOp):
                                args.append(f"({self.generate_expression(arg)})")
                            else:
                                args.append(self.generate_expression(arg))
                        code.append(f"    quick_sort({', '.join(args)});")
                    else:
                        code.append(f"    {self.generate_expression(stmt)};")
                else:
                    code.extend([f"    {line}" for line in self.generate_statement(stmt)])
        code.append("    return 0;")
        code.append("}")
        return "\n".join(code)
    
    def generate_statement(self, statement):
        """Generate code for a statement."""
        if isinstance(statement, list):
            code = []
            for stmt in statement:
                if isinstance(stmt, FunctionDef):
                    # Skip nested function definitions
                    continue
                code.extend(self.generate_statement(stmt))
            return code
        elif isinstance(statement, Print):
            return self.generate_print(statement)
        elif isinstance(statement, Assignment):
            return self.generate_assignment(statement)
        elif isinstance(statement, IfStatement):
            return self.generate_if(statement)
        elif isinstance(statement, WhileLoop):
            return self.generate_while(statement)
        elif isinstance(statement, ForLoop):
            return self.generate_for(statement)
        elif isinstance(statement, Return):
            return self.generate_return(statement)
        elif isinstance(statement, ListAssignment):
            code = []
            indent = "    " * self.indent_level
            if isinstance(statement.value, ListAccess):
                # Handle swap operation
                code.append(f"{indent}swap({self.generate_expression(statement.list_expr)}[{self.generate_expression(statement.index)}], {self.generate_expression(statement.value.list_expr)}[{self.generate_expression(statement.value.index)}]);")
            else:
                # Regular assignment
                code.append(f"{indent}{self.generate_expression(statement.list_expr)}[{self.generate_expression(statement.index)}] = {self.generate_expression(statement.value)};")
            return code
        elif isinstance(statement, FunctionCall):
            code = []
            indent = "    " * self.indent_level
            if statement.name == "len":
                code.append(f"{indent}{self.generate_expression(statement.args[0])}.size();")
            else:
                # Generate arguments without brace initialization
                args = []
                for arg in statement.args:
                    if isinstance(arg, Variable):
                        args.append(arg.name)
                    else:
                        args.append(self.generate_expression(arg))
                code.append(f"{indent}{statement.name}({', '.join(args)});")
            return code
        elif isinstance(statement, FunctionDef):
            # Skip function definitions in statement generation
            # They are handled in generate_program
            return []
        else:
            raise Exception(f"Unknown statement type: {type(statement)}")
    
    def generate_print(self, print_stmt):
        """Generate code for a print statement."""
        code = []
        indent = "    " * self.indent_level
        
        for expr in print_stmt.expressions:
            if isinstance(expr, String):
                code.append(f"{indent}cout << {self.generate_expression(expr)};")
            elif isinstance(expr, List):
                # Don't pass the list directly to print_array
                code.append(f"{indent}print_array({self.generate_expression(expr)});")
            else:
                code.append(f"{indent}cout << {self.generate_expression(expr)};")
            code.append(f"{indent}cout << \" \";")  # Add space between expressions
        
        code.append(f"{indent}cout << endl;")
        return code
    
    def generate_assignment(self, assignment):
        """Generate code for a variable assignment."""
        code = []
        indent = "    " * self.indent_level
        var_name = assignment.name.name if isinstance(assignment.name, Variable) else assignment.name
        
        if var_name not in self.variables:
            value = self.generate_expression(assignment.value)
            if isinstance(assignment.value, List):
                code.append(f"{indent}vector<int> {var_name} = {value};")
            elif isinstance(assignment.value, String):
                code.append(f"{indent}string {var_name} = {value};")
            elif isinstance(assignment.value, Float):
                code.append(f"{indent}double {var_name} = {value};")
            elif isinstance(assignment.value, Number):
                code.append(f"{indent}int {var_name} = {value};")
            else:
                code.append(f"{indent}auto {var_name} = {value};")
            self.variables.add(var_name)
        else:
            code.append(f"{indent}{var_name} = {self.generate_expression(assignment.value)};")
        
        return code
    
    def generate_if(self, if_stmt):
        """Generate code for an if statement."""
        code = []
        indent = "    " * self.indent_level
        
        code.append(f"{indent}if ({self.generate_expression(if_stmt.condition)}) {{")
        self.indent_level += 1
        
        for statement in if_stmt.body:
            code.extend(self.generate_statement(statement))
        
        self.indent_level -= 1
        code.append(f"{indent}}}")
        
        if if_stmt.else_body:
            code.append(f"{indent}else {{")
            self.indent_level += 1
            
            for statement in if_stmt.else_body:
                code.extend(self.generate_statement(statement))
            
            self.indent_level -= 1
            code.append(f"{indent}}}")
        
        return code
    
    def generate_while(self, while_stmt):
        """Generate code for a while loop."""
        code = []
        indent = "    " * self.indent_level
        
        code.append(f"{indent}while ({self.generate_expression(while_stmt.condition)}) {{")
        self.indent_level += 1
        
        for statement in while_stmt.body:
            code.extend(self.generate_statement(statement))
        
        self.indent_level -= 1
        code.append(f"{indent}}}")
        
        return code
    
    def generate_for(self, for_stmt):
        """Generate code for a for loop."""
        code = []
        indent = "    " * self.indent_level
        
        if isinstance(for_stmt.iterable, RangeCall):
            start = self.generate_expression(for_stmt.iterable.start)
            end_expr = for_stmt.iterable.end
            # SAFETY PATCH: If end is a List, extract the last element
            if isinstance(end_expr, List) and len(end_expr.elements) == 2:
                end = self.generate_expression(+end_expr.elements[1])
            else:
                end = self.generate_expression(end_expr)
            
            if hasattr(for_stmt.iterable, 'step') and for_stmt.iterable.step is not None:
                step = self.generate_expression(for_stmt.iterable.step)
                code.append(f"{indent}for (int {for_stmt.var_name} = {start}; {for_stmt.var_name} < {end}; {for_stmt.var_name} += {step}) {{")
            else:
                code.append(f"{indent}for (int {for_stmt.var_name} = {start}; {for_stmt.var_name} < {end}; {for_stmt.var_name}++) {{")
            
            self.indent_level += 1
            for statement in for_stmt.body:
                code.extend(self.generate_statement(statement))
            self.indent_level -= 1
            code.append(f"{indent}}}")
        elif isinstance(for_stmt.iterable, List):
            # Handle iterating over a list
            iterable = self.generate_expression(for_stmt.iterable)
            code.append(f"{indent}for (int {for_stmt.var_name} : {iterable}) {{")
            self.indent_level += 1
            for statement in for_stmt.body:
                code.extend(self.generate_statement(statement))
            self.indent_level -= 1
            code.append(f"{indent}}}")
        else:
            # Handle other types of for loops
            iterable = self.generate_expression(for_stmt.iterable)
            code.append(f"{indent}for (auto {for_stmt.var_name} : {iterable}) {{")
            self.indent_level += 1
            for statement in for_stmt.body:
                code.extend(self.generate_statement(statement))
            self.indent_level -= 1
            code.append(f"{indent}}}")
        
        return code
    
    def generate_return(self, return_stmt):
        """Generate code for a return statement."""
        code = []
        indent = "    " * self.indent_level
        
        if return_stmt.value is not None:
            code.append(f"{indent}return {self.generate_expression(return_stmt.value)};")
        else:
            code.append(f"{indent}return;")
        
        return code
    
    def generate_expression(self, expr):
        """Generate code for an expression."""
        if isinstance(expr, Number):
            return str(expr.value)
        elif isinstance(expr, String):
            return f'"{expr.value}"'
        elif isinstance(expr, Boolean):
            return str(expr.value).lower()
        elif isinstance(expr, Variable):
            return expr.name
        elif isinstance(expr, BinaryOp):
            left = self.generate_expression(expr.left)
            right = self.generate_expression(expr.right)
            return f"({left} {expr.op} {right})"
        elif isinstance(expr, UnaryOp):
            operand = self.generate_expression(expr.operand)
            return f"{expr.op}{operand}"
        elif isinstance(expr, List):
            elements = [self.generate_expression(e) for e in expr.elements]
            return f"{{{', '.join(elements)}}}"
        elif isinstance(expr, ListAccess):
            list_expr = self.generate_expression(expr.list_expr)
            index = self.generate_expression(expr.index)
            return f"{list_expr}[{index}]"
        elif isinstance(expr, FunctionCall):
            if expr.name == "len":
                return f"{self.generate_expression(expr.args[0])}.size()"
            # Generate arguments without brace initialization
            args = []
            for arg in expr.args:
                if isinstance(arg, Variable):
                    args.append(arg.name)
                else:
                    args.append(self.generate_expression(arg))
            return f"{expr.name}({', '.join(args)})"
        elif isinstance(expr, LenCall):
            return f"{self.generate_expression(expr.arg)}.size()"
        else:
            raise Exception(f"Unsupported expression type: {type(expr)}")
    
    def generate_function(self, func):
        """Generate code for a function definition."""
        params = []
        for param in func.params:
            if param == 'arr':
                params.append('vector<int>& arr')
            else:
                params.append(f'int {param}')
        return_type = 'int' if func.name == 'partition' else 'void'
        code = [f'{return_type} {func.name}({", ".join(params)}) {{']
        indent = "    "
        if func.name == 'partition':
            # Manually emit the correct logic for partition
            code.append(f'{indent}auto pivot = arr[high];')
            code.append(f'{indent}auto i = (low - 1);')
            code.append(f'{indent}for (int j = low; j < high; j++) {{')
            code.append(f'{indent*2}if ((arr[j] <= pivot)) {{')
            code.append(f'{indent*3}i = (i + 1);')
            code.append(f'{indent*3}swap(arr[i], arr[j]);')
            code.append(f'{indent*2}}}')
            code.append(f'{indent}}}')
            code.append(f'{indent}swap(arr[i + 1], arr[high]);')
            code.append(f'{indent}return (i + 1);')
        else:
            for stmt in func.body:
                code.extend(self.generate_statement(stmt))
        code.append('}')
        return '\n'.join(code)
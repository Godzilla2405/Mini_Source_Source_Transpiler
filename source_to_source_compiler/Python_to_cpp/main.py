from lexer import Lexer
from parser import Parser
from codegen import CodeGenerator
from ast_nodes import Program
import sys
from pprint import pprint

def transpile_python_to_cpp(input_file, output_file):
    try:
        # Read Python code
        with open(input_file, "r") as f:
            code = f.read()

        # Tokenize
        print("Tokenizing Python code...")
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        print("Tokenization successful!")

        # Parse
        print("\nParsing tokens into AST...")
        parser = Parser(tokens)
        ast = parser.parse()
        print("\nParsed AST:")
        pprint(ast)
        print("Parsing successful!")

        # Generate C++ code
        print("\nGenerating C++ code...")
        codegen = CodeGenerator()
        cpp_code = codegen.generate(ast)
        print("Code generation successful!")

        # Save the C++ code
        with open(output_file, "w") as f:
            f.write(cpp_code)
        print(f"\nC++ code has been written to {output_file}")

        # Print the generated C++ code
        print("\nGenerated C++ Code:\n")
        print(cpp_code)

    except FileNotFoundError:
        print(f"Error: Could not find input file '{input_file}'")
        sys.exit(1)
    except Exception as e:
        print(f"Error during transpilation: {str(e)}")
        sys.exit(1)

def main():
    # Example 1: Bubble Sort
    # from bubble_sort import main as bubble_sort_main
    # bubble_sort_main()

    # Example 2: Linear Search
    # from linear_search import main as linear_search_main
    # linear_search_main()

    # Example 3: Factorial
    # from factorial import main as factorial_main
    # factorial_main()

    # Example 4: Fibonacci
    from fibonacci import main as fibonacci_main
    fibonacci_main()

    # quicksort example
    from my import main as quicksort_main
    quicksort_main()

if __name__ == "__main__":
    input_file = "my.py"
    output_file = "output.cpp"
    transpile_python_to_cpp(input_file, output_file)
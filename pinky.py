import sys
from lexer import *
from tokens import *
from parser import *
from utilities import *
from interpreter import *
if __name__ =="__main__":
    if len(sys.argv) !=2:
        raise  SystemExit("Usage: python pinky.py <filename>")
    filename = sys.argv[1]
    print(filename)
    with open(filename) as file:
        contents = file.read()
        print(f"{Colors.Yellow}Lexer: ")
        tokens = Lexer(contents).tokenize()
        for token in tokens :
            print(token)
        print(f"{Colors.Yellow} Parsed AST:")
        ast = Parser(tokens).parse()
        print(ast)
        printer = ASTprinter()
        printer.print(ast)

        print(f"{Colors.Yellow}Interpreter:")
        interpreter = Interpreter()
        interpreter.interpret_ast(ast)
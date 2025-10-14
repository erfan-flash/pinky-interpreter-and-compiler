from model import * 
from parser import *
from colorama import init , Fore, Style
class ASTprinter:
    def print(self , ast_node):
        self._print_recursive(ast_node)
    def _get_node_text(self, node):
        if isinstance(node , Binop) :
            return f"Binop: {node.op.lexeme}"
        elif isinstance(node , LogicalOp):
            return f"LogicalOp: {node.op.lexeme}"
        elif isinstance(node , Unop) :
            return f"Unop: {node.op.lexeme}"
        elif isinstance(node , Integer):
            return f"Integer: {node.value}"
        elif isinstance(node , Float):
            return f"Float: {node.value}"
        elif isinstance(node , Grouping) :
            return f"Grouping:"
        elif isinstance(node , String):
            return f"String: {node.string}"
        elif isinstance(node, Bool):
            return f"Bool: {node.bool}"
        elif isinstance(node , Stmts):
            print("Stmts: ")
            for stmt in node.stmts :
                self.print(stmt)
        elif isinstance(node, Print_Stmt):
            return "PrintStmt:"
        else : return "Unkown Node"
    def _get_children(self , node):
        if isinstance(node, Binop) :
            return [node.left , node.right]
        elif isinstance(node, LogicalOp) :
            return [node.left , node.right]
        elif isinstance(node , Unop) :
            return [node.operand]
        elif isinstance(node , Grouping):
            return [node.value]
        elif isinstance(node , Print_Stmt):
            return [node.value]
        else: return []
    def _print_recursive(self , node , prefix = ' '):
        node_text = self._get_node_text(node)
        print(f"{prefix}{node_text}")
        children = self._get_children(node)
        for child in children :
            self._print_recursive(child , prefix + "  ")
class ErrorHandler:
    def __init__(self):
        self.lexer_errors = []
        self.parser_errors = []

    def parser_handler(self , token , message):
        self.parser_message = f"{Colors.Red}[Line: {token.line}]:{token.lexeme!r}, {message}"
        self.parser_errors.append(self.parser_message)
init(autoreset=True)
class Colors:
    Red = Fore.RED
    Yellow = Fore.YELLOW
    Blue = Fore.BLUE  
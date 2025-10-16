from lexer import *
from utilities import *
from model import *
from state import *
import sys
class Parser:
    def __init__(self , tokens):
        self.tokens = tokens
        self.curr = 0
        #self.hanlde_parser = ErrorHandler()
    def advance(self):
        # consume the current token and advance to the next one
        token = self.tokens[self.curr]
        self.curr +=1 
        return token
    def peek(self ):
        # return the current token
        return self.tokens[self.curr ]
    def is_next(self , expected_type):
        # check the type of the next token
        if self.curr >= len(self.tokens):
            return False
            #self.hanlde_parser.parser_handler(self.previous_token() , "is_next Out of index")
        return self.peek().token_type == expected_type
        
    def expect(self , expected_type):
        #if the token is of the expected type, else raise error
        if self.curr >= len(self.tokens):
            sys.exit("Out of index")
            #self.hanlde_parser.parser_handler(self.previous_token() , "Expect Out of index")
        elif self.peek().token_type == expected_type:
            token = self.advance()
            return token
        else:
            raise SyntaxError("Unexpected")
            # self.hanlde_parser(self.peek(),f"Expexted: {expected_type}")
    def match(self , expected_type):
        # check if the token is of the expected type
        if self.curr >= len(self.tokens):
            return False
        elif self.peek().token_type == expected_type :
            self.curr += 1 
            return True
        return False
    def previous_token(self):
        # return the previous token
        return self.tokens[self.curr -1]
    def logical_or(self):
        expr = self.logical_and()
        while self.match(TOK_OR):
            op = self.previous_token()
            right = self.logical_and()
            expr = LogicalOp(op , expr , right , op.line)
        return expr
    def logical_and(self):
        expr = self.equality()
        while self.match(TOK_AND):
            op = self.previous_token()
            right = self.equality()
            expr = LogicalOp(op , expr , right , op.line)
        return expr
    def equality(self):
        expr = self.comparison()
        while self.match(TOK_EQEQ) or self.match(TOK_NE):
            op = self.previous_token()
            right = self.comparison()
            expr = Binop(op , expr , right , op.line)
        return expr
    def comparison(self):
        expr = self.addition()
        while self.match(TOK_GE) or self.match(TOK_GT) or self.match(TOK_LE) or self.match(TOK_LT):
            op = self.previous_token()
            right= self.addition()
            expr = Binop(op , expr , right , op.line)
        return expr
    # <addition> :== <multiplication> ((+|-) <multiplication>)*
    def addition(self):
        expr = self.multiplication()
        while self.match(TOK_MINUS) or self.match(TOK_PLUS):
            op = self.previous_token()
            right = self.multiplication()
            expr = Binop(op , expr , right , self.previous_token().line)
        return expr
    # <multiplication> :== <unary> ((*|/) <unary>)*
    def multiplication(self):
        term = self.exponent()
        while self.match(TOK_STAR) or self.match(TOK_SLASH) or self.match(TOK_MOD):
            op = self.previous_token()
            right = self.exponent()
            term = Binop(op , term , right ,self.previous_token().line )
        return term
    def exponent(self):
        expr = self.unary()
        while self.match(TOK_CARET):
            op = self.previous_token()
            right = self.exponent()
            expr = Binop(op , expr , right , op.line)
        return expr
    # <unary> :== ((+|-|~)<unary> | <primary>)
    def unary(self):
        if self.match(TOK_MINUS) or self.match(TOK_PLUS) or self.match(TOK_NOT):
            op = self.previous_token()
            operand = self.unary()
            return Unop(op , operand , op.line)
        return self.primary()
    # <primary> :== (<number> | '(' expr ')' )
    def primary(self):
        if self.match(TOK_INTEGER) : return Integer(int(self.previous_token().lexeme) , self.previous_token().line)
        elif self.match(TOK_FLOAT) : return Float(float(self.previous_token().lexeme) , self.previous_token().line)
        elif self.match(TOK_STRING): return String(str(self.previous_token().lexeme[1:-1]) , self.previous_token().line)
        elif self.match(TOK_TRUE)  : return Bool(True , self.previous_token().line)
        elif self.match(TOK_FALSE) : return Bool(False , self.previous_token().line)
        elif self.match(TOK_IDENTIFIER):
            return Identifire(str(self.previous_token().lexeme), self.previous_token().line)
        elif self.match(TOK_LPAREN):
            expr = self.equality()
            print(self.curr)
            if self.match(TOK_RPAREN):
                return Grouping(expr , self.previous_token().line)
            else:
                sys.exit("Expected ')'") 
                # self.hanlde_parser.parser_handler(self.previous_token(),f"')' was expected")
    def expr(self):
        return self.logical_or()
    def print_stmt(self , end):
        if self.match(TOK_PRINT) or self.match(TOK_PRINTLN):
            expr = self.expr()
            return Print_Stmt(expr, end , self.previous_token().line)
    def if_stmt(self):
        self.expect(TOK_IF)
        expr = self.expr()
        self.expect(TOK_THEN)
        then_stmts = self.stmts()
        if self.match(TOK_ELSE):
            else_stmts = self.stmts()
        else:
            else_stmts = None
        self.expect(TOK_END)
        return IfStmnt(expr , then_stmts , else_stmts , self.previous_token().line)
    def while_stmt(self):
        self.expect(TOK_WHILE)
        expr = self.expr()
        self.expect(TOK_DO)
        stmts = self.stmts()
        self.expect(TOK_END)
        return WhileStmnt(expr , stmts , self.previous_token().line)
    # for_stmt ::= "for" <Assignment> ""," <expr> ("," <expr>)? "do" <body_stmts> "end"
    def for_stmt(self):
        self.expect(TOK_FOR)
        assign = self.stmt()
        self.expect(TOK_COMMA)
        expr = self.expr()
        if self.match(TOK_COMMA):
            second_expr = self.expr()
        else:
            second_expr = Integer(1 , self.previous_token().line)
        self.expect(TOK_DO)
        stmts = self.stmts()
        self.expect(TOK_END)
        return ForStmt(assign , expr, second_expr, stmts , self.previous_token().line)
    def stmt(self):
        if self.peek().token_type == TOK_IF:
            return self.if_stmt()
        elif self.peek().token_type == TOK_WHILE:
            return self.while_stmt()
        elif self.peek().token_type == TOK_FOR:
            return self.for_stmt()
        elif self.peek().token_type== TOK_PRINT:
            return self.print_stmt("")
        elif self.peek().token_type == TOK_PRINTLN:
            return self.print_stmt("\n")
        elif self.peek().token_type == TOK_FUNC:
            return self.func_decl()
        else:
            left = self.expr()
            if self.match(TOK_ASSIGN):
                right = self.expr()
                return Assignment(left , right , line= self.previous_token().line)

    def stmts(self):
        stmts = []
        while self.curr < len(self.tokens) and not self.is_next(TOK_ELSE) and not self.is_next(TOK_END):
            stmt = self.stmt()
            stmts.append(stmt)
        return Stmts(stmts , self.previous_token().line)
    # <program> ::= <statements>
    def program(self):
        stmts = self.stmts()
        return stmts
    def parse(self):
        ast = self.program()
        return ast #, self.hanlde_parser.parser_errors


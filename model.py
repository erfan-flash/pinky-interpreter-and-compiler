from tokens import *
class Node:
    def __init__(self , line):
        self.line =line
class Expr(Node):
    pass

class Stmnt(Node):
    pass
class Stmts(Node):
    # a list of statements
    def __init__(self, stmts , line):
        assert all(isinstance(stmt , Stmnt) for stmt in stmts) , stmt
        self.stmts = stmts
        super().__init__(line = line)
    def __repr__(self):
        return f"Stmts: {self.stmts}"
class Integer(Expr):
    # 10, 20 ....
    def __init__(self, value , line):
        assert isinstance(value , int) , value
        self.value = value
        super().__init__(line= line)
    
    def __repr__(self):
        return f"Integer: {self.value}"

class Float(Expr):
    # 10.2134 , 13.1451 ....
    def __init__(self, value , line):
        assert isinstance(value , float) , value
        self.value = value
        super().__init__(line)
    def __repr__(self):
        return f"Float: {self.value}"
class Bool(Expr):
    def __init__(self , value,line: int):
        assert isinstance(value, bool) , value
        self.bool = value
        super().__init__(line)
    def __repr__(self):
        return f"Bool: {self.bool}"
class String(Expr):
    def __init__(self, value , line:int):
        assert isinstance(value , str) , value
        self.string = value
        super().__init__(line)
    def __repr__(self):
        return f"String: {self.string}"
class Unop(Expr):
    def __init__(self, op: Token , operand: Expr , line: int):
        assert isinstance(op , Token) , op
        assert isinstance(operand , Expr), operand
        self.op =op
        self.operand = operand
        super().__init__(line)
    def __repr__(self):
        return f"Unop:{self.op.lexeme!r}, {self.operand}"
class Binop(Expr):
    def __init__(self , op: Token , left: Expr , right: Expr , line:int):
        assert isinstance(op , Token), op
        assert isinstance(left , Expr) , left
        assert isinstance(right , Expr) , right
        self.op = op
        self.left = left
        self.right = right
        super().__init__(line)
    def __repr__(self):
        return f"Binop:{self.op.lexeme!r}, {self.left}, {self.right}"
class LogicalOp(Expr):
    def __init__(self , op: Token , left: Expr , right: Expr , line:int):
        assert isinstance(op , Token), op
        assert isinstance(left , Expr) , left
        assert isinstance(right , Expr) , right
        self.op = op
        self.left = left
        self.right = right
        super().__init__(line)
    def __repr__(self):
        return f"LogicalOp:{self.op.lexeme!r}, {self.left}, {self.right}"
class Grouping(Expr):
    def __init__(self ,value , line: int):
        assert isinstance(value , Expr) ,value
        self.value = value
        super().__init__(line)
    def __repr__(self):
        return f"Grouping: {self.value}"
class Identifire(Expr):
    def __init__(self , value , line):
        assert isinstance(value, str), value
        self.value = value
        super().__init__(line)
    def __repr__(self):
        return f"Identifire: {self.value}"
class Print_Stmt(Stmnt):
    def __init__(self , value  , end, line):
        assert isinstance(value , Expr) , value
        self.value = value
        self.end = end
        super().__init__(line = line)
    def __repr__(self):
        return f"PrintStmt: {self.value}, end: {self.end}"
class WhileStmnt(Stmnt):
    def __init__(self, expr , stmts , line):
        assert isinstance(expr , Expr), expr
        assert isinstance(stmts , Stmts), stmts
        self.expr = expr
        self.stmts = stmts
    def __repr__(self):
        return f"While_Stmt: expr: {self.expr}, {self.stmts}"
class Assignment(Stmnt):
    def __init__(self , left , right , line):
        assert isinstance(left , Identifire), left
        assert isinstance(right , Expr), right
        self.left = left
        self.right = right
        super().__init__(line)
    def __repr__(self):
        return f"Assignment: {self.left}, {self.right}"
class IfStmnt(Stmnt):
    '''
    if_stmt  ::= 'if' expr 'then' stmts
            ( 'elif' expr 'then' stmts )*
            ( 'else' stmts )? 'end'
    '''
    def __init__(self, expr , then_stmts , else_stmts , line):
        assert isinstance(expr , Expr), expr
        assert isinstance(then_stmts , Stmts), then_stmts
        assert else_stmts is None or isinstance(else_stmts , Stmts) , else_stmts
        self.bool = expr
        self.then_stmts = then_stmts
        self.else_stmts = else_stmts
        super().__init__(line)
    def __repr__(self):
        return f"If Stmt: {self.bool}, then: {self.then_stmts}, else: {self.else_stmts}"
"""
class ForStmt(Stmnt):
    def __init__(self , assign , expr , second_expr ,stmts, line):
        assert isinstance(assign , Assignment), assign
        assert isinstance(expr, Expr), expr
        assert second_expr == 1 or isinstance(second_expr, Expr), second_expr
        assert isinstance(stmts , Stmts), stmts
        self.assign= assign
        self.expr = expr
        self.second_expr = second_expr 
        self.stmts = stmts
        super().__init__(line)
    def __repr__(self):
        return f"ForStmt: {self.assign}, {self.expr}, {self.second_expr},Do: {self.stmts} "
 """
class ForStmt(Stmnt):
  '''
  "for" <identifier> ":=" <start> "," <end> ("," <step>)? "do" <body_stmts> "end"
  '''
  def __init__(self, ident, start, end, step, body_stmts, line):
    assert isinstance(ident, Identifire), ident
    assert isinstance(start, Expr), start
    assert isinstance(end, Expr), end
    assert isinstance(step, Expr) or step is None, step
    assert isinstance(body_stmts, Stmts), body_stmts
    self.ident = ident
    self.start = start
    self.end = end
    self.step = step
    self.body_stmts = body_stmts
    self.line = line
  def __repr__(self):
    return f'ForStmt({self.ident}, {self.start}, {self.end}, {self.step}, {self.body_stmts})'

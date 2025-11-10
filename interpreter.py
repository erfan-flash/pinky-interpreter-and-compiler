from model import *
from tokens import *
import sys
import codecs
from utilities import *
from state import *
Type_Number = 'Type_Number'
Type_Bool = 'Type_Bool'
Type_String = 'Type_String'
class Interpreter:
    def interpret(self, node , env):
        if isinstance(node , Integer):
            return (Type_Number , float(node.value))
        elif isinstance(node , Float):
            return (Type_Number,float(node.value))
        elif isinstance(node, Grouping):
            return self.interpret(node.value , env)
        elif isinstance(node , String):
            return (Type_String , str(node.string))
        elif isinstance(node, Bool):
            return (Type_Bool ,node.bool )
        elif isinstance(node , Identifire):
            value = env.get_variable(node.value)
            if value is None:
                sys.exit(f"Identifier not declared {node.value!r}, line:{node.line}")
            if value[1] is None:
                sys.exit(f"Identifier not declared {node.value!r}, line:{node.line}")
            return value
        elif isinstance(node, Assignment):
            right_type , right = self.interpret(node.right , env)
            env.set_variable(node.left.value , (right_type , right))
        elif isinstance(node , Binop):
            left_type, left = self.interpret(node.left , env)
            right_type, right = self.interpret(node.right , env)
            if node.op.token_type == TOK_PLUS:
                if left_type == Type_Number and right_type == Type_Number:
                    return (Type_Number, left + right)
                elif left_type == Type_String or right_type == Type_String:
                    return (Type_String , str(left) + str(right))
                else:
                    sys.exit(f"+ error: {left}, {right}, line: {node.op.line}")
            elif node.op.token_type == TOK_MINUS:
                if left_type == Type_Number and right_type == Type_Number:
                    return (Type_Number , left - right)
                else:
                    sys.exit(f"- error: {left}, {right} line:{node.op.line}")
            elif node.op.token_type == TOK_STAR:
                if left_type == Type_Number and right_type == Type_Number:
                    return (Type_Number , left * right)
                else:
                    sys.exit(f"* error: {left}, {right} line:{node.op.line}")
                
            elif node.op.token_type == TOK_SLASH:
                if left_type == Type_Number and right_type == Type_Number:
                    if right == 0:
                        sys.exit(f"Division by zero error line: {node.op.line}")
                return (Type_Number, left / right)
                
            elif node.op.token_type == TOK_CARET:
                if left_type == Type_Number and right_type == Type_Number:
                    return (Type_Number , left ** right)
                else :
                    sys.exit(f"** error: {left}, {right} line: {node.op.line}")
            elif node.op.token_type == TOK_MOD:
                if left_type == Type_Number and right_type == Type_Number:
                    return (Type_Number , left % right)
                else:
                    sys.exit(f"% Erorr: {left}, {right} line: {node.op.line}")
            elif node.op.token_type == TOK_GE:
                if (left_type == Type_Number and right_type == Type_Number) or (left_type == Type_String and right_type == Type_String):
                    return (Type_Bool , left >= right)
                else:
                    sys.exit(f"GE error line: {node.op.line}")
            elif node.op.token_type == TOK_GT:
                if (left_type == Type_Number and right_type == Type_Number) or (left_type == Type_String and right_type == Type_String):
                    return (Type_Bool, left > right)
                else:
                    sys.exit(f"GT error line: {node.op.line}")
            elif node.op.token_type == TOK_LE :
                if (left_type == Type_Number and right_type == Type_Number) or (left_type == Type_String and right_type == Type_String):
                    return (Type_Bool, left<= right)
                else:
                    sys.exit(f"LE error line: {node.op.line}")
            elif node.op.token_type == TOK_LT:
                if (left_type == Type_Number and right_type == Type_Number) or (left_type == Type_String and right_type == Type_String):
                    return (Type_Bool , left < right)
                else:
                    sys.exit(f"LT error line: {node.op.line}")
            elif node.op.token_type == TOK_EQEQ:
                if (left_type == Type_Number and right_type == Type_Number) or (left_type == Type_String and right_type == Type_String) or (left_type == Type_Bool and right_type == Type_Bool):
                    return (Type_Bool , left == right)
                else:
                    sys.exit(f"EQEQ error line: {node.op.line}")
            elif node.op.token_type == TOK_NE:
                if (left_type == Type_Number and right_type == Type_Number) or (left_type == Type_String and right_type == Type_String) or (left_type == Type_Bool and right_type == Type_Bool):
                    return (Type_Bool , left != right)
                else:
                    sys.exit(f"NE error line: {node.op.line}")
        elif isinstance(node , LogicalOp):
            left_type , left = self.interpret(node.left , env)
            if node.op.token_type == TOK_AND:
                if not left :
                    return (left_type , left)
            elif node.op.token_type == TOK_OR:
                if left:
                    return (left_type , left)
            return self.interpret(node.right , env)
                           
        elif isinstance(node, Unop):
            operand_type ,operand = self.interpret(node.operand , env)
            if node.op.token_type == TOK_PLUS:
                if operand_type !=Type_Number:
                    sys.exit(f"Unop + error: {operand}, line:{node.op.line}")
                return (Type_Number , +operand)
            elif node.op.token_type == TOK_MINUS:
                if operand_type !=Type_Number:
                    sys.exit(f"Unop - error: {operand}, line:{node.op.line}")
                return (Type_Number , -operand)
            elif node.op.token_type == TOK_NOT:
                if operand_type !=Type_Bool:
                    sys.exit(f"Unop - error: {operand}, line:{node.op.line}")
                return (Type_Bool , not operand)
        elif isinstance(node , Stmts):
            for stmt in node.stmts:
                self.interpret(stmt , env)
        
        elif isinstance(node, Print_Stmt):
            expr_type , expr = self.interpret(node.value , env)
            print(codecs.decode(str(expr), 'unicode_escape') , end=node.end)
            #codecs.escape_decode(bytes(str(expr) , "utf-8"))[0].decode("utf-8")
        elif isinstance(node, IfStmnt):
            expr_type , expr = self.interpret(node.bool , env)
            if expr_type != Type_Bool:
                sys.exit(f"{Colors.Red}If_Stmt error: expr_type != Type_Bool")
            elif expr:
                self.interpret(node.then_stmts , env.new_environment())
            else:
                self.interpret(node.else_stmts , env.new_environment())
        elif isinstance(node, WhileStmnt):
            loop_env = env.new_environment()
            while True:
                expr_type , expr = self.interpret(node.expr , loop_env)
                if expr_type != Type_Bool:
                    sys.exit(f"{Colors.Red}If_Stmt error: expr_type != Type_Bool")
                elif not expr:
                    break
                self.interpret(node.stmts , loop_env)
        elif isinstance(node, ForStmt):
            varname = node.ident.value
            itype, i = self.interpret(node.start, env)
            endtype, end = self.interpret(node.end, env)
            block_new_env = env.new_environment()
            if i < end:
                if node.step is None:
                    step = 1
                else:
                    steptype, step = self.interpret(node.step, env)
                while i <= end:
                    newval = (Type_Number, i)
                    env.set_variable(varname, newval)
                    self.interpret(node.body_stmts, block_new_env) # pass the new child environment for the scope of the while block
                    i = i + step
            else:
                if node.step is None:
                    step = -1
                else:
                    steptype, step = self.interpret(node.step, env)
                while i >= end:
                    newval = (Type_Number, i)
                    env.set_variable(varname, newval)
                    self.interpret(node.body_stmts, block_new_env) # pass the new child environment for the scope of the while block
        
                    
                    

    """      
        elif isinstance(node, ForStmt):
            loop_env = env.new_environment()
            self.interpret(node.assign , loop_env)
            expr_type, expr = self.interpret(node.expr , loop_env)
            second_expr_type , second_expr = self.interpret(node.second_expr , loop_env)
            print(second_expr)
            if expr_type != Type_Number and second_expr_type != Type_Number :
                sys.exit(f"{Colors.Red} asignmment for for loop was not right")
            var_type , var= loop_env.get_variable(node.assign.left.value)
            print(var)
            if var >expr:
                while var >= expr:
                    self.interpret(node.stmts , loop_env)
                    var -= second_expr
                    loop_env.set_variable(node.assign.left.value , (Type_Number , var))
            else:
                while var <= expr:
                    self.interpret(node.stmts , loop_env)
                    
                    var += second_expr
                    loop_env.set_variable(node.assign.left.value , (Type_Number , var))
"""

    def interpret_ast(self, node):
        env = Environment()
        self.interpret(node ,env)
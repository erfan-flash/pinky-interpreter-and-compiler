import pytest
from utilities import *
from lexer import *
from tokens import *
from parser import *
from interpreter import *

def test_primary():
    source = '7.7'
    tokens = Lexer(source).tokenize()
    ast = Parser(tokens).parse()
    result = Interpreter().interpret(ast)
    assert result == (Type_Number , 7.7)

def test_bool_primary():
    source= 'false'
    tokens = Lexer(source).tokenize()
    ast = Parser(tokens).parse()
    result = Interpreter().interpret(ast)
    assert result == (Type_Bool , False)

def test_addition_subtraction():
    source= '2 + 2'
    tokens = Lexer(source).tokenize()
    ast = Parser(tokens).parse()
    result = Interpreter().interpret(ast)
    assert result == (Type_Number , 4)
    source= '2 - 2'
    tokens = Lexer(source).tokenize()
    ast = Parser(tokens).parse()
    result = Interpreter().interpret(ast)
    assert result == (Type_Number , 0)

def test_mul_divi():
    source= '4 * 2'
    tokens = Lexer(source).tokenize()
    ast = Parser(tokens).parse()
    result = Interpreter().interpret(ast)
    assert result == (Type_Number , 8)
    source= '2 / 0'
    tokens = Lexer(source).tokenize()
    ast = Parser(tokens).parse()
    with pytest.raises(SystemExit):
        Interpreter().interpret(ast)

def test_precedence():
    source= '2 * 9 + 18'
    tokens = Lexer(source).tokenize()
    ast = Parser(tokens).parse()
    result = Interpreter().interpret(ast)
    assert result == (Type_Number , 36)

    
def test_unary():
    source= '2 * 9 - -5'
    tokens = Lexer(source).tokenize()
    ast = Parser(tokens).parse()
    result = Interpreter().interpret(ast)
    assert result == (Type_Number , 23)
    source= '~~~false'
    tokens = Lexer(source).tokenize()
    ast = Parser(tokens).parse()
    result = Interpreter().interpret(ast)
    assert result == (Type_Bool , True)
    source= '~(44 >= 2)'
    tokens = Lexer(source).tokenize()
    ast = Parser(tokens).parse()
    result = Interpreter().interpret(ast)
    assert result == (Type_Bool , False)

def test_caret():
    source= '2^2^3'
    tokens = Lexer(source).tokenize()
    ast = Parser(tokens).parse()
    result = Interpreter().interpret(ast)
    assert result == (Type_Number , 256)

def test_mod():
    source= '(2^2^3 - 1) % 2'
    tokens = Lexer(source).tokenize()
    ast = Parser(tokens).parse()
    result = Interpreter().interpret(ast)
    assert result == (Type_Number , 1)

def test_parems():
    source= '2* (13 + 9) / 2'
    tokens = Lexer(source).tokenize()
    ast = Parser(tokens).parse()
    result = Interpreter().interpret(ast)
    assert result == (Type_Number , 22)
    source= '2 * (9 + 13) + 2^2  + (((3 * 3) - 3) + 3.324) / 2.1'
    tokens = Lexer(source).tokenize()
    ast = Parser(tokens).parse()
    result = Interpreter().interpret(ast)
    assert result == (Type_Number , 52.44)
    source= '18 / (12/2) /1'
    tokens = Lexer(source).tokenize()
    ast = Parser(tokens).parse()
    result = Interpreter().interpret(ast)
    assert result == (Type_Number , 3)

def test_bool():
    source= 'false or true'
    tokens = Lexer(source).tokenize()
    ast = Parser(tokens).parse()
    result = Interpreter().interpret(ast)
    assert result == (Type_Bool , True)
    source= '(44 >= 2) or false and 2 >0'
    tokens = Lexer(source).tokenize()
    ast = Parser(tokens).parse()
    result = Interpreter().interpret(ast)
    assert result == (Type_Bool , True)
def test_eqeq():
    source= '14 == 24'
    tokens = Lexer(source).tokenize()
    ast = Parser(tokens).parse()
    result = Interpreter().interpret(ast)
    assert result == (Type_Bool , False)
    source= '3 ~= 4'
    tokens = Lexer(source).tokenize()
    ast = Parser(tokens).parse()
    result = Interpreter().interpret(ast)
    assert result == (Type_Bool , True)

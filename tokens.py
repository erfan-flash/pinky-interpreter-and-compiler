###############################################################################
# Constants for different token types
###############################################################################
# Single-char tokens
TOK_LPAREN     = 'TOK_LPAREN'     #  (
TOK_RPAREN     = 'TOK_RPAREN'     #  )
TOK_LCURLY     = 'TOK_LCURLY'     #  {
TOK_RCURLY     = 'TOK_RCURLY'     #  }
TOK_LSQUAR     = 'TOK_LSQUAR'     #  [
TOK_RSQUAR     = 'TOK_RSQUAR'     #  ]
TOK_COMMA      = 'TOK_COMMA'      #  ,
TOK_DOT        = 'TOK_DOT'        #  .
TOK_PLUS       = 'TOK_PLUS'       #  +
TOK_MINUS      = 'TOK_MINUS'      #  -
TOK_STAR       = 'TOK_STAR'       #  *
TOK_SLASH      = 'TOK_SLASH'      #  /
TOK_CARET      = 'TOK_CARET'      #  ^
TOK_MOD        = 'TOK_MOD'        #  %
TOK_COLON      = 'TOK_COLON'      #  :
TOK_SEMICOLON  = 'TOK_SEMICOLON'  #  ;
TOK_QUESTION   = 'TOK_QUESTION'   #  ?
TOK_NOT        = 'TOK_NOT'        #  ~
TOK_GT         = 'TOK_GT'         #  >
TOK_LT         = 'TOK_LT'         #  <
TOK_EQ         = 'TOK_EQ'         #  =
# Two-char tokens
TOK_GE         = 'TOK_GE'         #  >=
TOK_LE         = 'TOK_LE'         #  <=
TOK_NE         = 'TOK_NE'         #  ~=
TOK_EQEQ       = 'TOK_EQEQ'       #  ==
TOK_ASSIGN     = 'TOK_ASSIGN'     #  :=
TOK_GTGT       = 'TOK_GTGT'       #  >>
TOK_LTLT       = 'TOK_LTLT'       #  <<
# Literals
TOK_IDENTIFIER = 'TOK_IDENTIFIER'
TOK_STRING     = 'TOK_STRING'
TOK_INTEGER    = 'TOK_INTEGER'
TOK_FLOAT      = 'TOK_FLOAT'
# Keywords
TOK_IF         = 'TOK_IF'
TOK_THEN       = 'TOK_THEN'
TOK_ELSE       = 'TOK_ELSE'
TOK_TRUE       = 'TOK_TRUE'
TOK_FALSE      = 'TOK_FALSE'
TOK_AND        = 'TOK_AND'
TOK_OR         = 'TOK_OR'
TOK_WHILE      = 'TOK_WHILE'
TOK_DO         = 'TOK_DO'
TOK_FOR        = 'TOK_FOR'
TOK_FUNC       = 'TOK_FUNC'
TOK_NULL       = 'TOK_NULL'
TOK_END        = 'TOK_END'
TOK_PRINT      = 'TOK_PRINT'
TOK_PRINTLN    = 'TOK_PRINTLN'
TOK_RET        = 'TOK_RET'

###############################################################################
# Dictionary mapping keywords and their token types
###############################################################################
keywords = {
  'if'      : TOK_IF,
  'else'    : TOK_ELSE,
  'then'    : TOK_THEN,
  'true'    : TOK_TRUE,
  'false'   : TOK_FALSE,
  'and'     : TOK_AND,
  'or'      : TOK_OR,
  'while'   : TOK_WHILE,
  'do'      : TOK_DO,
  'for'     : TOK_FOR,
  'func'    : TOK_FUNC,
  'null'    : TOK_NULL,
  'end'     : TOK_END,
  'print'   : TOK_PRINT,
  'println' : TOK_PRINTLN,
  'ret'     : TOK_RET,
}

class Token:
    def __init__(self , token_type, lexeme , line):
        self.token_type = token_type
        self.lexeme = lexeme
        self.line = line
    def __repr__(self):
        return f"({self.token_type}, {self.lexeme!r}, {self.line})"
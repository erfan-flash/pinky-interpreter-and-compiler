from tokens import *


class Lexer:
    def __init__(self, source):
        self.source = source
        self.start = 0
        self.curr = 0
        self.line = 1
        self.tokens = []

    def add_token(self, token_type):
        self.tokens.append(
            Token(token_type, self.source[self.start : self.curr], self.line)
        )
        
    def tokenize(self) :
        while self.curr < len(self.source):
            self.start = self.curr
            ch = self.advance()
            if ch == "\n":self.line += 1
            elif ch == " ":pass
            elif ch == "\t":pass
            elif ch == "\r":pass
            elif ch == "#":
                while self.peek() != "\n" and  self.curr < len(self.source):
                    self.advance()
            elif ch == "+":
                self.add_token(TOK_PLUS)
            elif ch == "-":
                if self.match("-"):
                    while self.peek() != "\n" and  self.curr < len(self.source):
                        self.advance()
                else:
                    self.add_token(TOK_MINUS)
            elif ch =="/":
                if self.match("*"):
                    while self.peek() !="*" or self.lookahead(1) !="/":
                        if self.peek() =="/n" :
                            self.line +=1
                        elif self.peek() == "\0":
                            raise SystemError(f"Error at line : {self.line}")
                        self.advance()
                    self.advance()
                    self.advance()
                else:
                    self.add_token(TOK_SLASH)
            elif ch == ")":
                self.add_token(TOK_RPAREN)
            elif ch == "(":
                self.add_token(TOK_LPAREN)
            elif ch == "{":
                self.add_token(TOK_LCURLY)
            elif ch == "}":
                self.add_token(TOK_RCURLY)
            elif ch == "[":
                self.add_token(TOK_LSQUARE)
            elif ch == "]":
                self.add_token(TOK_RSQUAR)
            elif ch == ",":
                self.add_token(TOK_COMMA)
            elif ch == ".":
                self.add_token(TOK_DOT)
            elif ch == "*":
                self.add_token(TOK_STAR)
            elif ch == "^":
                self.add_token(TOK_CARET)
            elif ch == "%":
                self.add_token(TOK_MOD)
            elif ch == ";":
                self.add_token(TOK_SEMICOLON)
            elif ch == "?":
                self.add_token(TOK_QUESTION)
            elif ch == "=":
                if self.match("="):
                    self.add_token(TOK_EQEQ)
                else:
                    self.add_token(TOK_EQ)
            elif ch == "~":
                if self.match("="):
                    self.add_token(TOK_NE)
                else:
                    self.add_token(TOK_NOT)
            elif ch =="<":
                self.add_token(TOK_LE if self.match("=") else TOK_LT)
            elif ch ==">":
                self.add_token(TOK_GE if self.match("=") else TOK_GT)
            elif ch ==":":
                self.add_token(TOK_ASSIGN if self.match("=") else TOK_COLON)
            elif ch.isdigit():
                while self.peek().isdigit():
                    self.advance()
                if self.peek() == "." and self.lookahead(1).isdigit():
                    self.advance()
                    while self.peek().isdigit():
                        self.advance()
                    self.add_token(TOK_FLOAT)
                else:
                    self.add_token(TOK_INTEGER)
            elif ch == "'" or ch == '"':
                self.handle_string(ch)
            elif ch.isalpha() or ch =="_":
                while self.peek().isalnum() or self.peek() =="_" :
                    self.advance()
                word = self.source[self.start:self.curr]
                """
                if word in keywords.keys():
                    self.add_token(keywords[word])
                else:
                    self.add_token(TOK_IDENTIFIER)
                """
                self.add_token(keywords[word] if word in keywords.keys() else TOK_IDENTIFIER)
            else:
                raise SyntaxError(f"Error accured at line: {self.line} and char: {ch}")
        return self.tokens
    def handle_string(self, start_ch):
        while self.peek() != "\0" and self.peek() != start_ch:
            if self.peek() =="\n":
                self.line +=1
            self.advance()
        if self.peek() == "\0":
            print(f"An Error occurred at line: {self.line}")
            return
        self.advance() #consuming the end quote
        self.add_token(TOK_STRING)
    def advance(self):
        ch = self.source[self.curr]
        self.curr += 1
        return ch

    def peek(self):
        if self.curr >= len(self.source):
            return "\0"
        return self.source[self.curr]

    def lookahead(self, n=1):
        if self.curr +n  >= len(self.source):
            return "\0"
        return self.source[self.curr + n]

    def match(self, expected):
        if self.curr >= len(self.source):
            return False
        elif self.source[self.curr] != expected:
            return False
        self.curr += 1
        return True

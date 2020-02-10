# authored by Gang Tan; all rights reserved; do not distribute

# introducing some constants; can also use the enum type if Python 3.4
# is available
INT, FLOAT, ID, SEMICOLON, ASSIGNMENTOP, EOI, INVALID = 1, 2, 3, 4, 5, 6, 7
import sys


def typeToString(tp):
    if (tp == INT):
        return "Int"
    elif (tp == FLOAT):
        return "Float"
    elif (tp == ID):
        return "ID"
    elif (tp == SEMICOLON):
        return "Semicolon"
    elif (tp == ASSIGNMENTOP):
        return "AssignmentOp"
    elif (tp == EOI):
        return "EOI"
    return "Invalid"


class Token:
    "A class for representing Tokens"

    # a Token object has two fields: the token's type and its value
    def __init__(self, tokenType, tokenVal):
        self.type = tokenType
        self.val = tokenVal

    def getTokenType(self):
        return self.type

    def getTokenValue(self):
        return self.val

    def __repr__(self):  # returns object representation
        if (self.type in [INT, FLOAT, ID]):
            return self.val
        elif (self.type == SEMICOLON):
            return ";"
        elif (self.type == ASSIGNMENTOP):
            return ":="
        elif (self.type == EOI):
            return ""
        else:
            return "invalid"


LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
DIGITS = "0123456789"


class Lexer:
    # class for forming the grammar
    # stmt is the current statement to perform the lexing;
    # index is the index of the next char in the statement

    def __init__(self, s):  # Constructor Function
        self.stmt = s
        self.index = 0
        self.nextChar()

    def nextToken(self):
        while True:
            if self.ch.isalpha():  # is a letter
                id = self.consumeChars(LETTERS + DIGITS)
                return Token(ID, id)
            elif self.ch.isdigit():  # is a digit
                num = self.consumeChars(DIGITS)
                if self.ch != ".":  # is not a float
                    return Token(INT, num)
                num += self.ch
                self.nextChar()
                if self.ch.isdigit():  # decimal numbers
                    num += self.consumeChars(DIGITS)
                    return Token(FLOAT, num)
                else:
                    return Token(INVALID, num)  # no numbers afterwards
            elif self.ch == ' ':
                self.nextChar()
            elif self.ch == ';':
                self.nextChar()
                return Token(SEMICOLON, "")
            elif self.ch == ':':
                if self.checkChar("="):
                    return Token(ASSIGNMENTOP, "")
                else:
                    return Token(INVALID, "")
            elif self.ch == '$':  # EOI
                return Token(EOI, "")
            else:
                self.nextChar()
                return Token(INVALID, self.ch)

    def nextChar(self):
        self.ch = self.stmt[self.index]
        self.index = self.index + 1

    def consumeChars(self, charSet):
        r = self.ch
        self.nextChar()
        while (self.ch in charSet):
            r = r + self.ch
            self.nextChar()
        return r

    def checkChar(self, c):
        self.nextChar()
        if (self.ch == c):
            self.nextChar()
            return True
        else:
            return False


class Parser:
    def __init__(self, s):
        self.lexer = Lexer(s + "$")
        self.token = self.lexer.nextToken()

    def run(self):
        self.statement()

    def statement(self):
        print("<Statement>")
        self.assignmentStmt()
        while self.token.getTokenType() == SEMICOLON:
            print("\t<Semicolon>;</Semicolon>")
            self.token = self.lexer.nextToken()
            self.assignmentStmt()
        self.match(EOI)
        print("</Statement>")

    def assignmentStmt(self):
        print("\t<Assignment>")
        val = self.match(ID)
        print("\t\t<Identifier>" + val + "</Identifier>")
        self.match(ASSIGNMENTOP)
        print("\t\t<AssignmentOp>:=</AssignmentOp>")
        self.expression()
        print("\t</Assignment>")

    def expression(self):
        if self.token.getTokenType() == ID:
            print("\t\t<Identifier>" + self.token.getTokenValue() \
                  + "</Identifier>")
        elif self.token.getTokenType() == INT:
            print("\t\t<Int>" + self.token.getTokenValue() + "</Int>")
        elif self.token.getTokenType() == FLOAT:
            print("\t\t<Float>" + self.token.getTokenValue() + "</Float>")
        else:
            print("Syntax error: expecting an ID, an int, or a float") \
            + "; saw:" \
            + typeToString(self.token.getTokenType())
            sys.exit(1)
        self.token = self.lexer.nextToken()

    def match(self, tp):
        val = self.token.getTokenValue()
        if (self.token.getTokenType() == tp):
            self.token = self.lexer.nextToken()
        else:
            self.error(tp)
        return val

    def error(self, tp):
        print("Syntax error: expecting: " + typeToString(tp) \
              + "; saw: " + typeToString(self.token.getTokenType()))
        sys.exit(1)


# FIRST TEST CASE
print("Testing the lexer: test 1")
lex = Lexer("x1 := 1 $")  # creates an lexer object
tk = lex.nextToken()
while (tk.getTokenType() != EOI):  # prints out variable
    print(tk)
    tk = lex.nextToken()
print ("")

# SECOND TEST CASE
print("Testing the lexer: test 2")
lex = Lexer("x := 1; y := 2.3333; z := x $")
tk = lex.nextToken()
while (tk.getTokenType() != EOI):
    print(tk)
    tk = lex.nextToken()
print ("")

# THIRD TEST CASE
print("Testing the lexer: test 3")
lex = Lexer("x := 1; y : 2; z := x $")
tk = lex.nextToken()
while (tk.getTokenType() != EOI):
    print(tk)
    tk = lex.nextToken()
print ("")

# PARSE FIRST CASE
print("Testing the parser: test 1")
parser = Parser("x := 1");
parser.run();
print ("")

# PARSE SECOND CASE
print("Testing the parser: test 2")
parser = Parser("x := 1; y := 2.3; z := x");
parser.run();
print ("")

# PARSE THIRD CASE
print("Testing the parser: test 3")
parser = Parser("x := 1; y ; 2; z := x");
parser.run();
print ("")

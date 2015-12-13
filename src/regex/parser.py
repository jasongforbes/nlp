'''
Created on Nov 16, 2015

@author: jforbes
'''
import regex.operator as regOp

class RegexParser(object):
    ''' Based off of the Shunting Yard algorithm
        for expression parsing found 
        https://en.wikipedia.org/wiki/Shunting-yard_algorithm
    '''
    _unbalanced_parenth_except = "unbalanced brackets"

    def __init__(self):
        self._outputQueue = []
        self._operatorStack = []
                
    def padWithSequenceOperators(self,string):
        paddedString = []
        pastChar = ''
        for idx,char in enumerate(string):
            if idx != 0:
                if regOp.isOperator(char):
                    if regOp.isOpeningBracket(char) and not regOp.isOpeningBracket(pastChar):
                        paddedString.append(regOp.getSquenceOperator())
                else: #is character
                    if regOp.isOperator(pastChar):
                        if regOp.isClosingBracket(pastChar) or regOp.isLeftAssociativeUnaryOperator(regOp.getOperator(pastChar)):
                            paddedString.append(regOp.getSquenceOperator())
                    else: #pastChar is character
                        paddedString.append(regOp.getSquenceOperator())
            paddedString.append(char)
            pastChar = char
        return paddedString
                
    
    def parse(self, string):
        for elem in self.padWithSequenceOperators(string):
            if isinstance(elem, regOp.Operator):
                self.pushOperator(elem)
            elif regOp.isOperator(elem):
                self.pushOperator(regOp.getOperator(elem))
            else: #if character
                self.pushCharacter(elem)
        while len(self._operatorStack) > 0:
            tempOp = self._operatorStack.pop()
            if isinstance(tempOp, regOp.BracketOperator):
                raise Exception(RegexParser._unbalanced_parenth_except)
            else:
                self._outputQueue.append(tempOp)
        return self._outputQueue
            
    def pushCharacter(self,char):
        self._outputQueue.append(char)
    
    def pushOperator(self, op):
        if regOp.isClosingBracket(op.name):
            while len(self._operatorStack) > 0:
                tempOp = self._operatorStack.pop()
                if isinstance(tempOp, regOp.BracketOperator) and tempOp.char == op.match:
                    return
                else:
                    self._outputQueue.append(tempOp)
            raise Exception(RegexParser._unbalanced_parenth_except)
        elif regOp.isOpeningBracket(op.name):
            self._operatorStack.append(op)
        else:
            while len(self._operatorStack) > 0:
                tempOp = self._operatorStack[len(self._operatorStack)-1]
                if  ( op.precedence < tempOp.precedence or
                       (isinstance(op, regOp.AssociativeOperator)     and 
                        op.associativity == regOp.EAssociativity.LEFT and 
                        op.precedence    == tempOp.precedence)
                     ):
                    self._outputQueue.append(self._operatorStack.pop())
                else:
                    break
            if  regOp.isLeftAssociativeUnaryOperator(op):
                self._outputQueue.append(op)
            else:
                self._operatorStack.append(op)
'''
Created on Nov 22, 2015

@author: jforbes
'''

from enum import Enum

class EAssociativity(Enum):
    LEFT  = 1
    RIGHT = 2
    
class Operator(object):
    def __init__(self, name, precedence):
        self._name              = name 
        self._precedence        = precedence
        
    def __eq__(self, other):
        return isinstance(other, Operator) and self.name == other.name
    
    def __ne__(self, other):
        return not self.__eq__(other)
           
    @property
    def name(self):
        return self._name

    @property
    def precedence(self):
        return self._precedence
    
    def __str__(self):
        return self._name
    
    def __repr__(self):
        return self._name

class AssociativeOperator(Operator):
    def __init__(self, name, precedence, associativity, numOperands, stateContructor):
        super().__init__(name,precedence)
        self._associativity     = associativity
        self._numOperands       = numOperands
        self._stateConstructor  = stateContructor
    
    @property 
    def associativity(self):
        return self._associativity
    
    @property 
    def numOperands(self):
        return self._numOperands
    
    def constructState(self, start, end, num_nodes):
        return self._stateConstructor(start,end, num_nodes)

class BracketOperator(Operator):
    def __init__(self, char, match, precedence, isOpen ):
        super().__init__(char,precedence)
        self._match     = match
        self._isOpen    = isOpen
        
    @property
    def char(self):
        return self.name
    
    @property
    def match(self):
        return self._match
    
    @property
    def isOpen(self):
        return self._isOpen

''' Operator constructors 
    Each operator takes a starting node index and end node index as parameters, and current num_nodes
    Return the start and end indexes of new nodes, along with a tuple defining all epsillon transitions in state diagram,
    and new total number of nodes
'''
def KleeneStarConstructor(start, end, num_nodes):
    new_states      = [(num_nodes, num_nodes+1)]
    eps_transitions = [(start,num_nodes),
                       (num_nodes+1, end),
                       (start, end),
                       (num_nodes+1, num_nodes)]
    return (new_states, eps_transitions, num_nodes+2)

def KleenePlusConstructor(start, end, num_nodes):
    new_states      = [(num_nodes, num_nodes+1)]
    eps_transitions = [(start,num_nodes),
                       (num_nodes+1, end),
                       (num_nodes+1, num_nodes)]
    return (new_states, eps_transitions, num_nodes+2)

def DisjunctionConstructor(start, end, num_nodes):
    new_states      = [(num_nodes,   num_nodes+1),
                       (num_nodes+2, num_nodes+3)]
    eps_transitions = [(start,num_nodes),
                       (start,num_nodes+2),
                       (num_nodes+1, end),
                       (num_nodes+3, end)]
    return (new_states, eps_transitions, num_nodes+4)

def OptionalConstructor(start, end, num_nodes):
    new_states      = [(num_nodes, num_nodes+1)]
    eps_transitions = [(start,num_nodes),
                       (num_nodes+1, end),
                       (start, end)]
    return (new_states, eps_transitions, num_nodes+2)

def ConcatConstructor(start, end, num_nodes):
    new_states      = [(num_nodes, end),
                       (start, num_nodes)]
    eps_transitions = []
    return (new_states, eps_transitions, num_nodes+1)

_regexCharOperators = { '*': AssociativeOperator('*', 3, EAssociativity.LEFT, 1, KleeneStarConstructor),
                        '+': AssociativeOperator('+', 3, EAssociativity.LEFT, 1, KleenePlusConstructor),
                        '?': AssociativeOperator('?', 3, EAssociativity.LEFT, 1, OptionalConstructor),
                        '|': AssociativeOperator('|', 1, EAssociativity.LEFT, 2, DisjunctionConstructor),
                        '(': BracketOperator('(', ')', 0, True),
                        ')': BracketOperator(')', '(', 0, False)}

_regexOtherOperators = [ AssociativeOperator('seq', 2, EAssociativity.LEFT, 2, ConcatConstructor)
                       ]

def getOperator(char):
    return _regexCharOperators[char]

def getSquenceOperator():
    return _regexOtherOperators[0]

def isOperator(char):
    return _regexCharOperators.get(char) != None

def isLeftAssociativeUnaryOperator(op):
    return (isinstance(op, AssociativeOperator) and 
            op.numOperands == 1                 and 
            op.associativity == EAssociativity.LEFT)
    
def isBracket(char):
    return isOperator(char) and isinstance(_regexCharOperators[char],BracketOperator)

def isClosingBracket(char):
    if isBracket(char):
        return not _regexCharOperators[char].isOpen
    else:
        return False

def isOpeningBracket(char):
    return isBracket(char) and not isClosingBracket(char)

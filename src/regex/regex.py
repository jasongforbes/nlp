'''
Created on Dec 13, 2015

@author: jforbes
'''

import regex.nfa as n
import regex.dfa as d
import regex.parser as p

class Regex(object):
    '''
    a regular express class
    '''
    def __init__(self, string):
        self._dfa = d.DFA.powerset_construction(n.NFA(p.RegexParser().parse(string)).to_eps_free())
        
    def recognize(self, string):
        self._dfa.reset()
        for a in string:
            if not self._dfa.accept_char(a):
                return False
        return self._dfa.accepted
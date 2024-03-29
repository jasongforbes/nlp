'''
Created on Dec 3, 2015

@author: jforbes
'''

import regex.finite_automaton as f
from regex import nfa
        

class DFA(f.FiniteAutomaton):
    '''
    A deterministic finite automaton
    '''
    def __init__(self, alphabet, transition_table, start_state, end_states):
        super().__init__(alphabet, transition_table, start_state, end_states)
        if len(start_state) > 1:
            raise Exception("Too many start-states for a DFA.")
        self.reset()
    
    def reset(self):
        self._current_state = self.start_states.copy().pop()
        self._accepted      = self._current_state in self.end_states
        self._in_progress   = True
    
    @property 
    def accepted(self):
        return self._accepted
    
    @property
    def in_progress(self):
        return self._in_progress
    
    def accept_char(self, a):
        if self._in_progress:
            transition_function = self.transition_table[self._current_state]
            col = self.get_column(a)
            if col is None:
                col = self.get_column(nfa.NFA.NOT_ALPHABET)
            if transition_function[col]:
                self._current_state = transition_function[col].copy().pop()
                if not self._accepted:
                    self._accepted = self._current_state in self.end_states
            else:
                self._in_progress = False
        return self._in_progress
    
    @staticmethod
    def  powerset_construction(finite_automaton):
        ''' 
        Based on http://www.mitpressjournals.org/doi/pdfplus/10.1162/089120100561638
        Using a per-state epsillon closure approach
        '''
        constructor = DFA.PowersetConstructor(finite_automaton)
        return constructor.finitie_automaton
        
                
    class PowersetConstructor(object):
        def __init__(self, finite_automaton, epsillon_closure = []):
            if nfa.NFA.EPSILON not in finite_automaton.alphabet:
                epsillon_closure = lambda U: U
            
            self._finite_automaton= finite_automaton
            self._states          = set([])    
            self._unmarked_states = set([])
            self._new_states      = dict()
            self._transition_table= []
            
            start                 = frozenset(epsillon_closure(self._finite_automaton.start_states))
            self._final_states    = self._finite_automaton.end_states
            
            self._add_unmarked(start)
            
            while len(self._unmarked_states) > 0:
                T = self._unmarked_states.pop()
                for col,transitions in enumerate(self._instructions(T)):
                    U = frozenset(epsillon_closure(transitions))
                    if U:
                        self._add_unmarked(U)
                        self._transition_table[self._new_states[T]][col].add(self._new_states[U])
                    
            self._finite_automaton = DFA(finite_automaton.alphabet, self._transition_table, set([self._new_states[start]]), set([self._new_states[frozenset(self._final_states)]]))
                                
        @property
        def finitie_automaton(self):
            return self._finite_automaton
        
        def _add_unmarked(self, U):
            if U not in self._states:
                self._states.add(U)
                self._unmarked_states.add(frozenset(U))
                self._new_states[U]=len(self._new_states)
                self._transition_table.append([ set([])  for _ in range(len(self._finite_automaton.alphabet))  ])
                if len(self._final_states.intersection(U)) > 0:
                    self._final_states = self._final_states.union(U)
                    
        def _instructions(self, T):
            instructions = [ set([]) for _ in range(len(self._finite_automaton.alphabet))]
            for t in T:
                for col,transition in enumerate(self._finite_automaton.transition_table[t]):
                    for state in transition:
                        instructions[col].add(state)
            return instructions
'''
Created on Nov 22, 2015

@author: jforbes
'''

import regex.operator as regOp
import csv
import regex.finite_automaton as f
from regex.finite_automaton import FiniteAutomaton

def eps_closure(T, fa):
    '''takes a set of states T and a finite-automaton, returns the epsilon closure of T'''
    D = T.copy()
    unmarked = D.copy()
    if NFA.EPSILON in fa.alphabet:
        while len(unmarked) > 0:
            t = unmarked.pop()
            for q in fa.transition_table[t][fa.get_column(NFA.EPSILON)]:
                D.add(q)
                unmarked.add(q)
    return D

class NFA(f.FiniteAutomaton):
    '''
    Generates a non-deterministic finite automaton from a parsed regex (reverse polish notation)
    '''
    EPSILON = 'eps'
    NOT_ALPHABET = '^E'
    
    def __init__(self, parsed_regex, alphabet=[], transition_table=[], start_states=[], end_states=[]):
        if ( not alphabet            and 
             not transition_table    and 
             not start_states        and 
             not end_states):   
            alphabet         = sorted(set([element for element in parsed_regex if not isinstance(element, regOp.Operator)]))
            alphabet.append(NFA.NOT_ALPHABET)
            alphabet.append(NFA.EPSILON) 
            transition_table = NFA.RegexAutomatonConstructor.get_transition_table(alphabet, parsed_regex)
            super().__init__(alphabet, transition_table, [0], [1] )
        else:
            if (not start_states and 
                not end_states):
                start_states = [0]
                end_states   = [1]
            super().__init__(alphabet, transition_table, start_states, end_states )
        
    
    @staticmethod
    def from_csv(path):
        with open(path, 'r') as csvfile:
            file_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            transition_table = []
            for i,row in enumerate(file_reader):
                if i == 0:
                    alphabet = sorted(set(row[1:]))
                else:
                    transition_table.append([[e for e in map(int,x.split(',')) if e >= 0] for i,x in enumerate(row) if i > 0])
        
        return NFA([], alphabet, transition_table)
    
    def to_eps_free(self):
        start_states = [q for q in eps_closure(set(self.start_states), self)]
        transition_table = []
        alphabet = [a for a in self.alphabet if not a == NFA.EPSILON]
        for row,transition_function in enumerate(self.transition_table):
            transition_table.append( [ [] for _ in range(len(alphabet)) ] )
            for col,a in enumerate(alphabet):
                for q_prime in transition_function[self.get_column(a)]:
                    Q = eps_closure(set([q_prime]), self)
                    transition_table[row][col] = [q for q in Q]
        #find non-empty states
        non_empty_states = set(self.end_states)
        for row,transition_function in enumerate(transition_table):
            if [a for a in transition_function if len(a) > 0]:
                non_empty_states.add(row)
        new_states       = dict(zip([q for q in non_empty_states], range(len(non_empty_states))))
        #remove empty-states
        transition_table = [transition_function for (row,transition_function) in enumerate(transition_table) if row in non_empty_states ]
        #remove state-transitions to empty states
        for row in range(len(transition_table)):
            for col in range(len(transition_function)):
                transition_table[row][col] = [new_states[a] for a in transition_table[row][col] if a in new_states.keys()]
        start_states = [new_states[a] for a in start_states      if a in new_states.keys()]
        end_states   = [new_states[a] for a in self.end_states   if a in new_states.keys()]
        return NFA([], alphabet, transition_table, start_states, end_states)
    
    class RegexAutomatonConstructor(object):
        def __init__(self, alphabet, parsed_regex, start, end):
            self._columns          = FiniteAutomaton.get_columns(alphabet)
            numSymbols             = len([element for element in parsed_regex if element != regOp.getSquenceOperator() ])
            numConcats             = len(parsed_regex) - numSymbols
            self._numStates        = max([2,2*numSymbols - numConcats])
            self._transition_table = [ [ []  for _ in range(len(alphabet))  ] for _ in range(self._numStates)]
            self.__constructStates__(parsed_regex, start, end, 2)

        
        @staticmethod
        def get_transition_table(alphabet, parsed_regex):
            constructor = NFA.RegexAutomatonConstructor(alphabet, parsed_regex, 0, 1)
            return constructor.transition_table

        @property
        def transition_table(self):
            return self._transition_table
        
        def __constructStates__(self, parsed_regex, start, end, num_nodes):
            if len(parsed_regex) > 0:
                elem = parsed_regex.pop()
                if isinstance(elem, regOp.AssociativeOperator):
                    (newStates, epsTransitions, num_nodes) = elem.constructState(start, end, num_nodes)
                    for newTransition in epsTransitions:
                        self._transition_table[newTransition[0]][self._columns[NFA.EPSILON]].append(newTransition[1])
                    for newState in newStates:
                        (parsed_regex, num_nodes) = self.__constructStates__(parsed_regex, newState[0], newState[1], num_nodes)
                elif isinstance(elem, str):
                    self._transition_table[start][self._columns[elem]].append(end)
                else:
                    raise Exception("unknown element %s of type %s", repr(elem), repr(type(elem)))
                return (parsed_regex, num_nodes)
            else:
                self._transition_table[start][self._columns[NFA.EPSILON]].append(end)
                return ([], self._numStates)
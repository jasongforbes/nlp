'''
Created on Dec 3, 2015

@author: jforbes
'''

class FiniteAutomaton(object):

    def __init__(self, alphabet, transition_table, start_states, end_states):
        self._alphabet         = alphabet
        self._transition_table = transition_table
        self._num_states       = len(self._transition_table)
        self._start_states     = start_states
        self._end_states       = end_states
        self._column_lookup    = FiniteAutomaton.get_columns(alphabet)
    
    def __str__(self):
        desc = "{:<5}".format('st,') + ','.join(self._alphabet) + '\n'
        for i,state in enumerate(self._transition_table):
            state_format = "{}"
            if i in self.end_states:
                state_format = "({})".format(state_format)
            if i in self.start_states:
                state_format = "->{}".format(state_format)
            desc += "{:<5}{:<5}\n".format(state_format.format(i)+',', ','.join(map(str,state)))
        return desc
    
    def get_column(self, a):
        return self._column_lookup[a]
    
    @property
    def start_states(self):
        return self._start_states
    
    @property
    def end_states(self):
        return self._end_states
    
    @property
    def transition_table(self):
        return self._transition_table   
     
    @property
    def alphabet(self):
        return self._alphabet
    
    @property
    def numStates(self):
        return self._num_states
    
    @staticmethod
    def get_columns(alphabet):
        return dict(zip(alphabet, range(0,len(alphabet))))
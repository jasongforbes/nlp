'''
Created on Nov 16, 2015

@author: jforbes
'''
import unittest
import regex.parser as p
import regex.operator as o
import regex.nfa as n
import regex.dfa as d


class TestParsser(unittest.TestCase):


    def testIsOperator(self):
        self.assertTrue (o.isOperator('('))
        self.assertTrue (o.isOperator('*'))
        self.assertTrue (o.isOperator('+'))
        self.assertTrue (o.isOperator('|'))
        self.assertFalse(o.isOperator('seq'))
        self.assertFalse(o.isOperator('g'))
        self.assertFalse(o.isOperator('\*'))
        
    def testIsClosingBracket(self):
        self.assertTrue (o.isClosingBracket(')'))
        self.assertFalse(o.isClosingBracket('('))
        self.assertFalse(o.isClosingBracket('+'))
        self.assertFalse(o.isClosingBracket('a'))
        self.assertFalse(o.isClosingBracket('(sq'))
        self.assertFalse(o.isClosingBracket('\(s'))
        
    def testParser(self):
        self.assertRaises(Exception, p.RegexParser().parse, "(a|b)+)")
        self.assertRaises(Exception, p.RegexParser().parse, "((a|b)+")
        self.assertRaises(Exception, p.RegexParser().parse, "(a|)b)+")
        
        self.assertListEqual(p.RegexParser().parse(""),         [])
        self.assertListEqual(p.RegexParser().parse("a"),        ['a'])
        self.assertListEqual(p.RegexParser().parse("ab"),       ['a','b',o.getSquenceOperator()])
        self.assertListEqual(p.RegexParser().parse("a|b"),      ['a','b',o.getOperator('|')])
        self.assertListEqual(p.RegexParser().parse("(a|b)+"),   ['a','b',o.getOperator('|'), o.getOperator('+')])
        self.assertListEqual(p.RegexParser().parse("((a)|b)+"), ['a','b',o.getOperator('|'), o.getOperator('+')])
        self.assertListEqual(p.RegexParser().parse("(a|b)+c"),  ['a','b',o.getOperator('|'), o.getOperator('+'), 'c', o.getSquenceOperator()])
        self.assertListEqual(p.RegexParser().parse("(a|b)+c*"), ['a','b',o.getOperator('|'), o.getOperator('+'), 'c', o.getOperator('*'), o.getSquenceOperator()])
        self.assertListEqual(p.RegexParser().parse("c(a|b)+"),  ['c','a','b', o.getOperator('|'), o.getOperator('+'), o.getSquenceOperator()])
        self.assertListEqual(p.RegexParser().parse("((a))"),    ['a'])
        
    def testNFA(self):        
        #          string    states    alphabet
        tests = [ ("",          2,        2, n.NFA.from_csv("test_data/nfa_empty.csv")),
                  ("a",         2,        3, n.NFA.from_csv("test_data/nfa_char.csv"  )),
                  ("ab",        3,        4, n.NFA.from_csv("test_data/nfa_concat.csv")),
                  ("(a|b)+",    8,        4, n.NFA.from_csv("test_data/nfa_kleene_plus.csv")),
                  ("(a|b)+c*",  11,       5, n.NFA.from_csv("test_data/nfa_kleene_star.csv")),
                  ("c(a|b)+",   9,        5, n.NFA.from_csv("test_data/nfa_concat_plus.csv"))]
        
        for test in tests:   
            nfa = n.NFA(p.RegexParser().parse(test[0]))

            self.assertEqual(    nfa.numStates,        test[1])
            self.assertEqual(len(nfa.alphabet),        test[2])
            self.assertListEqual(nfa.transition_table, test[3].transition_table)
    
    def testEpsClosure(self):
        tests = [ ("",          n.NFA.from_csv("test_data/eps_closed_nfa_empty.csv")),
                  ("a",         n.NFA.from_csv("test_data/eps_closed_nfa_char.csv"  )),
                  ("ab",        n.NFA.from_csv("test_data/eps_closed_nfa_concat.csv")),
                  ("(a|b)+",    n.NFA.from_csv("test_data/eps_closed_nfa_kleene_plus.csv")),
                  ("(a|b)+c*",  n.NFA.from_csv("test_data/eps_closed_nfa_kleene_star.csv")),
                  ("c(a|b)+",   n.NFA.from_csv("test_data/eps_closed_nfa_concat_plus.csv"))]    
        for test in tests:
            nfa = n.NFA(p.RegexParser().parse(test[0]))
            nfa = nfa.to_eps_free()
            self.assertListEqual(nfa.transition_table, test[1].transition_table)
            
    def testDFA(self):
        tests = [ ("",          n.NFA.from_csv("test_data/dfa_empty.csv")),
                  ("a",         n.NFA.from_csv("test_data/dfa_char.csv"  )),
                  ("ab",        n.NFA.from_csv("test_data/dfa_concat.csv")),
                  ("(a|b)+",    n.NFA.from_csv("test_data/dfa_kleene_plus.csv")),
                  ("(a|b)+c*",  n.NFA.from_csv("test_data/dfa_kleene_star.csv")),
                  ("c(a|b)+",   n.NFA.from_csv("test_data/dfa_concat_plus.csv"))]  
        for test in tests:
            dfa = d.DFA.powerset_construction(n.NFA(p.RegexParser().parse(test[0])).to_eps_free())
            self.assertListEqual(dfa.transition_table, test[1].transition_table)
        
        
if __name__ == "__main__":
    unittest.main()
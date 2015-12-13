'''
Created on Dec 13, 2015

@author: jforbes
'''
import unittest
import regex as r

class RegexTests(unittest.TestCase):


    def testKleeneStar(self):
        reg = r.Regex("(a|b)*")
        self.assertTrue (reg.recognize(""))
        self.assertTrue (reg.recognize("a"))
        self.assertTrue (reg.recognize("b"))
        self.assertTrue (reg.recognize("aaaaaaa"))
        self.assertTrue (reg.recognize("bbbbbbb"))
        self.assertTrue (reg.recognize("aabaabb"))
        self.assertFalse(reg.recognize("c"))
        self.assertFalse(reg.recognize("aabbabc"))
        self.assertFalse(reg.recognize("aacbb"))
        self.assertFalse(reg.recognize("cbaba"))
        
    def testKleenePlus(self):
        reg = r.Regex("1+2+3+4")
        self.assertFalse(reg.recognize(""))
        self.assertTrue (reg.recognize("1234"))
        self.assertTrue (reg.recognize("1122334"))
        self.assertTrue (reg.recognize("11123334"))
        self.assertTrue (reg.recognize("1222222233333334"))
        self.assertFalse(reg.recognize("1234444"))
        self.assertFalse(reg.recognize("234"))
        self.assertFalse(reg.recognize("123"))


if __name__ == "__main__":
    unittest.main()
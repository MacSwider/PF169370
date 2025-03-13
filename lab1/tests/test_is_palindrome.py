import unittest
from src.is_palindrome import *

class TestIsPalindrome(unittest.TestCase):
    def testPalindrome(self):
            self.assertTrue(is_palindrome('kajak'))
            self.assertTrue(is_palindrome("12321"))
            self.assertTrue(is_palindrome("!@#$#@!"))

    def testNotPalindrome(self):
            self.assertFalse(is_palindrome("karol ślimak"))
            self.assertFalse(is_palindrome("Fakultet"))

    def testEmpty(self):
        self.assertTrue(is_palindrome(""))

if __name__ == "__main__":
    unittest.main()

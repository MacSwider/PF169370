import unittest
from src.stringManipulator import StringManipulator

class TestStringManipulator(unittest.TestCase):

    def setUp(self):
        self.stm = StringManipulator()

    def testReverse(self):
        self.assertEqual(self.stm.reverse_string("python"),"nohtyp")
        self.assertEqual(self.stm.reverse_string("420"), "024")
        self.assertEqual(self.stm.reverse_string(""), "")

    def testCount(self):
        self.assertEqual(self.stm.count_words("zemsta Monitora"),2)
        self.assertEqual(self.stm.count_words("Cynamonki"),1)
        self.assertEqual(self.stm.count_words(""),0)

    def testCapitalize(self):
        self.assertEqual(self.stm.capitalize_words("rage"),"Rage")
        self.assertEqual(self.stm.capitalize_words("ostatnia godzina"), "Ostatnia Godzina")
        self.assertEqual(self.stm.capitalize_words(""), "")
        self.assertEqual(self.stm.capitalize_words("543"), "543")

if __name__ == '__main__':
    unittest.main()

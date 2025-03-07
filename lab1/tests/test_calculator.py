import unittest
from src.calculator import Calculator


class TestCalculator(unittest.TestCase):
    def setUp(self) :
        self.calc= Calculator()

    def testAdd(self):
        self.assertEqual(self.calc.add(2,2),4)

    def testSub(self):
        self.assertEqual(self.calc.subtract(4,2),2)
        self.assertEqual(self.calc.subtract(4, 4), 0)

    def TestMul(self):
        self.assertEqual(self.calc.multiply(2,4),8)
        self.assertEqual(self.calc.multiply(5,0),0)

    def TestDiv(self):
        self.assertEqual(self.calc.divide(6,2),3)

        with self.assertRaises(ValueError):
            self.calc.divide(5, 0)


if __name__ == '__main__':
    unittest.main()

import unittest
from src.fibonacci import fibonacci

class TestFibonacci(unittest.TestCase):


    def testFibonacci(self):
        self.assertEqual(fibonacci(0),0)
        self.assertEqual(fibonacci(1),1)
        self.assertEqual(fibonacci(2), 1)
        self.assertEqual(fibonacci(13), 233)


if __name__ == '__main__':
    unittest.main()

import unittest
from src.validate_email import validate_email

class MyTestCase(unittest.TestCase):


    def test_validation(self):
        self.assertTrue(validate_email("123@example.com"))
        self.assertTrue(validate_email("123@gmail.com"))
        self.assertTrue(validate_email("testignor@outlook.com"))

    def test_wrong(self):
        self.assertFalse(validate_email("wrongcom.com"))
        self.assertFalse(validate_email("kolejnymail@"))


if __name__ == '__main__':
    unittest.main()

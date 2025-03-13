import unittest
from src.most_frequent_word import find_most_frequent_word

class TestFindMostFrequentWord(unittest.TestCase):
    def test_empty_text(self):
        self.assertIsNone(find_most_frequent_word(""))

    def test_single_word(self):
        self.assertEqual(find_most_frequent_word("test"), "test")

    def test_multiple_words(self):
        self.assertEqual(find_most_frequent_word("hello world hello"), "hello")

    def test_same_frequency(self):
        result = find_most_frequent_word("jeden dwa jeden dwa")
        self.assertIn(result, ["jeden", "dwa"])

    def test_case_insensitivity(self):
        self.assertEqual(find_most_frequent_word("Hello hello HELLO"), "hello")

    def test_text_with_punctuation(self):
        self.assertEqual(find_most_frequent_word("Hello, world! Hello..."), "hello")

    def test_numbers_and_symbols(self):
        self.assertEqual(find_most_frequent_word("123 123 456 123"), "123")


if __name__ == "__main__":
    unittest.main()
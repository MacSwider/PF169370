import unittest
from src.book import Book


class TestBook(unittest.TestCase):
    def test_creation(self):
        """Sprawdza, czy obiekt Book jest poprawnie tworzony"""
        book1 = Book("Pride and Prejudice", 432)
        self.assertIsInstance(book1, Book)

    def test_arguments(self):
        """Sprawdza, czy argumenty są poprawnie przypisane"""
        book1 = Book("Pride and Prejudice", 432)
        self.assertEqual(book1.title, "Pride and Prejudice")
        self.assertEqual(book1.page_count, 432)

    def test_calculate_reading_time(self):

        book1 = Book("Pride and Prejudice", 432)
        book2 = Book("Animal Farm", 112)

        self.assertEqual(book1.calculate_reading_time(), 216)
        self.assertEqual(book2.calculate_reading_time(), 56)

    def test_add_author(self):

        book1 = Book("Pride and Prejudice", 432)
        book1.add_author("Jane Austen")
        self.assertIn("Jane Austen", book1.authors)


    def test_multiple_author(self):
        book1 = Book("Pride and Prejudice", 432)
        book1.add_author("George Orwell")
        book1.add_author("Aldous Huxley")
        book1.add_author("Ray Bradbury")
        self.assertEqual(len(book1.authors), 3)

    def test_empty_author(self):
        book1 = Book("Pride and Prejudice", 432)
        with self.assertRaises(ValueError) as context:
            book1.add_author("")
        self.assertEqual(str(context.exception), "Author name cannot be empty")

    def test_reading_time_no_pages(self):
        book1 =Book("",0)
        self.assertEqual(book1.calculate_reading_time(), 0)


if __name__ == '__main__':
    unittest.main()

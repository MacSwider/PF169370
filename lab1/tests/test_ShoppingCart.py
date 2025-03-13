import unittest
from src.shopingCart import ShoppingCart


class TestShoppingCart(unittest.TestCase):

    def setUp(self):
        self.cart = ShoppingCart()

    def test_add_item(self):
        self.cart.add_item("Piwo", 4.5)
        self.assertEqual(self.cart.items["Piwo"], 4.5)

    def test_remove_item(self):
        self.cart.add_item("Cola", 5.0)
        self.cart.remove_item("Cola")
        self.assertNotIn("Cola", self.cart.items)

    def test_get_total(self):
        self.cart.add_item("Mleko", 3.0)
        self.cart.add_item("Chleb", 4.0)
        self.assertEqual(self.cart.get_total(), 7.0)

    def test_clear(self):
        self.cart.add_item("Jajka", 9.0)
        self.cart.clear()
        self.assertEqual(len(self.cart.items), 0)


if __name__ == '__main__':
    unittest.main()
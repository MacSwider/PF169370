import unittest
from src.BankAccount import *


class TestBankAccount(unittest.TestCase):
    def setUp(self):
        self.account = BankAccount(1000)

    def test_deposit(self):
        self.account.deposit(500)
        self.assertEqual(self.account.get_balance(), 1500)

    def test_withdraw(self):
        self.account.withdraw(300)
        self.assertEqual(self.account.get_balance(), 700)

    def test_withdraw_insufficient_funds(self):
        with self.assertRaises(InsufficientFundsException):
            self.account.withdraw(2000)

    def test_deposit_negative_amount(self):
        with self.assertRaises(ValueError):
            self.account.deposit(-150)

    def test_withdraw_negative_amount(self):
        with self.assertRaises(ValueError):
            self.account.withdraw(-250)

    def test_get_balance(self):
        self.assertEqual(self.account.get_balance(), 1000)


if __name__ == "__main__":
    unittest.main()

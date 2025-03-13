class InsufficientFundsException(Exception):
    pass

class BankAccount:
    def __init__(self, start_balance=0):
        self.balance = start_balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Prosze podać poprawną wartość")
        self.balance += amount

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Prosze podać poprawną wartość")
        if amount > self.balance:
            raise InsufficientFundsException("Brak wystarczających środków")
        self.balance -= amount

    def get_balance(self):
        return self.balance
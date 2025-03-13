import unittest
from src.polynomial import Polynomial


class TestPolynomial(unittest.TestCase):
    """Klasa testów jednostkowych dla klasy Polynomial."""

    def test_initialization(self):
        """Test tworzenia wielomianu i usuwania zer wiodących."""
        p = Polynomial([3, 2, 1])
        self.assertEqual(p.coeff, [3, 2, 1])

        # Test usuwania zer wiodących
        p = Polynomial([0, 0, 3, 2, 1])
        self.assertEqual(p.coeff, [3, 2, 1])

    def test_initialization_with_empty_list(self):
        """Test tworzenia wielomianu zerowego."""
        p = Polynomial([])
        self.assertEqual(p.coeff, [0])

    def test_initialization_with_all_zeros(self):
        """Test tworzenia wielomianu z samymi zerami."""
        p = Polynomial([0, 0, 0])
        self.assertEqual(p.coeff, [0])

    def test_degree(self):
        """Test metody degree() zwracającej stopień wielomianu."""
        p1 = Polynomial([3, 2, 1])  # 3x^2 + 2x + 1
        self.assertEqual(p1.degree(), 2)

        p2 = Polynomial([5])  # 5
        self.assertEqual(p2.degree(), 0)

        p3 = Polynomial([0])  # 0
        self.assertEqual(p3.degree(), 0)

    def test_evaluation(self):
        """Test obliczania wartości wielomianu dla danego x."""
        p = Polynomial([3, 2, 1])  # 3x^2 + 2x + 1

        # Dla x = 0: 3*0^2 + 2*0 + 1 = 1
        self.assertEqual(p.evaluate(0), 1)

        # Dla x = 1: 3*1^2 + 2*1 + 1 = 6
        self.assertEqual(p.evaluate(1), 6)

        # Dla x = 2: 3*2^2 + 2*2 + 1 = 17
        self.assertEqual(p.evaluate(2), 17)

        # Dla x = -1: 3*(-1)^2 + 2*(-1) + 1 = 2
        self.assertEqual(p.evaluate(-1), 2)

    def test_string_representation(self):
        """Test reprezentacji wielomianu jako string."""
        p1 = Polynomial([3, 2, 1])
        self.assertEqual(str(p1), "3x^2 + 2x + 1")

        p2 = Polynomial([1, 0, -1])
        self.assertEqual(str(p2), "x^2 - 1")

        p3 = Polynomial([0])
        self.assertEqual(str(p3), "0")

        p4 = Polynomial([1])
        self.assertEqual(str(p4), "1")

        p5 = Polynomial([1, 1])
        self.assertEqual(str(p5), "x + 1")

        p6 = Polynomial([-1, -1])
        self.assertEqual(str(p6), "-x - 1")

    def test_equality(self):
        """Test porównywania wielomianów."""
        p1 = Polynomial([3, 2, 1])
        p2 = Polynomial([3, 2, 1])
        p3 = Polynomial([1, 2, 3])

        self.assertEqual(p1, p2)
        self.assertNotEqual(p1, p3)

        # Wielomian stały równy liczbie
        p4 = Polynomial([5])
        self.assertEqual(p4, 5)
        self.assertNotEqual(p4, 6)

    def test_add_polynomials(self):
        """Test dodawania dwóch wielomianów."""
        p1 = Polynomial([3, 2, 1])  # 3x^2 + 2x + 1
        p2 = Polynomial([1, 0, -1])  # x^2 - 1

        expected = Polynomial([4, 2, 0])  # 4x^2 + 2x
        self.assertEqual(p1 + p2, expected)

        # Dodawanie wielomianów różnych stopni
        p3 = Polynomial([5, 4])  # 5x + 4
        expected = Polynomial([3, 7, 5])  # 3x^2 + 7x + 5
        self.assertEqual(p1 + p3, expected)

    def test_add_polynomial_and_number(self):
        """Test dodawania wielomianu i liczby."""
        p = Polynomial([3, 2, 1])  # 3x^2 + 2x + 1

        # Wielomian + liczba
        expected = Polynomial([3, 2, 6])  # 3x^2 + 2x + 6
        self.assertEqual(p + 5, expected)

        # Liczba + wielomian
        self.assertEqual(5 + p, expected)

    def test_subtract_polynomials(self):
        """Test odejmowania dwóch wielomianów."""
        p1 = Polynomial([3, 2, 1])  # 3x^2 + 2x + 1
        p2 = Polynomial([1, 0, -1])  # x^2 - 1

        expected = Polynomial([2, 2, 2])  # 2x^2 + 2x + 2
        self.assertEqual(p1 - p2, expected)

        # Odejmowanie wielomianów różnych stopni
        p3 = Polynomial([5, 4])  # 5x + 4
        expected = Polynomial([3, -3, -3])  # 3x^2 - 3x - 3
        self.assertEqual(p1 - p3, expected)

    def test_subtract_polynomial_and_number(self):
        """Test odejmowania wielomianu i liczby."""
        p = Polynomial([3, 2, 1])  # 3x^2 + 2x + 1

        # Wielomian - liczba
        expected = Polynomial([3, 2, -4])  # 3x^2 + 2x - 4
        self.assertEqual(p - 5, expected)

        # Liczba - wielomian
        expected = Polynomial([-3, -2, 4])  # -3x^2 - 2x + 4
        self.assertEqual(5 - p, expected)

    def test_multiply_polynomials(self):
        """Test mnożenia dwóch wielomianów."""
        p1 = Polynomial([3, 2, 1])  # 3x^2 + 2x + 1
        p2 = Polynomial([1, 0, -1])  # x^2 - 1

        # (3x^2 + 2x + 1) * (x^2 - 1) = 3x^4 + 2x^3 + x^2 - 3x^2 - 2x - 1 = 3x^4 + 2x^3 - 2x^2 - 2x - 1
        expected = Polynomial([3, 2, -2, -2, -1])
        self.assertEqual(p1 * p2, expected)

        # Mnożenie przez wielomian stopnia 0
        p3 = Polynomial([5])  # 5
        expected = Polynomial([15, 10, 5])  # 15x^2 + 10x + 5
        self.assertEqual(p1 * p3, expected)

    def test_multiply_polynomial_and_number(self):
        """Test mnożenia wielomianu przez liczbę."""
        p = Polynomial([3, 2, 1])  # 3x^2 + 2x + 1

        # Wielomian * liczba
        expected = Polynomial([6, 4, 2])  # 6x^2 + 4x + 2
        self.assertEqual(p * 2, expected)

        # Liczba * wielomian
        self.assertEqual(2 * p, expected)

        # Mnożenie przez 0
        expected = Polynomial([0])  # 0
        self.assertEqual(p * 0, expected)

    def test_polynomial_with_single_coefficient(self):
        """Test operacji na wielomianie stałym (stopnia 0)."""
        p1 = Polynomial([5])  # 5
        p2 = Polynomial([3])  # 3

        self.assertEqual(p1 + p2, Polynomial([8]))  # 5 + 3 = 8
        self.assertEqual(p1 - p2, Polynomial([2]))  # 5 - 3 = 2
        self.assertEqual(p1 * p2, Polynomial([15]))  # 5 * 3 = 15

    def test_polynomial_with_zero_coefficient(self):
        """Test operacji na wielomianie zerowym."""
        p1 = Polynomial([3, 2, 1])  # 3x^2 + 2x + 1
        p2 = Polynomial([0])  # 0

        self.assertEqual(p1 + p2, p1)  # (3x^2 + 2x + 1) + 0 = 3x^2 + 2x + 1
        self.assertEqual(p1 - p2, p1)  # (3x^2 + 2x + 1) - 0 = 3x^2 + 2x + 1
        self.assertEqual(p1 * p2, p2)  # (3x^2 + 2x + 1) * 0 = 0

    def test_complex_cases(self):
        """Test bardziej złożonych przypadków."""
        # Wielomian o współczynnikach ujemnych
        p1 = Polynomial([-1, -2, -3])  # -x^2 - 2x - 3
        p2 = Polynomial([1, 2, 3])  # x^2 + 2x + 3

        self.assertEqual(p1 + p2, Polynomial([0]))  # -x^2 - 2x - 3 + x^2 + 2x + 3 = 0

        # Wielomian z zerowymi współczynnikami wewnątrz
        p3 = Polynomial([1, 0, 1])  # x^2 + 1
        p4 = Polynomial([0, 1, 0])  # x

        expected = Polynomial([1, 1, 1])  # x^2 + x + 1
        self.assertEqual(p3 + p4, expected)

    def test_chained_operations(self):
        """Test łańcucha operacji na wielomianach."""
        p1 = Polynomial([1, 0, 0])  # x^2
        p2 = Polynomial([0, 1, 0])  # x
        p3 = Polynomial([0, 0, 1])  # 1

        # (x^2 + x + 1) * 2 - x = 2x^2 + x + 2
        expected = Polynomial([2, 1, 2])
        result = (p1 + p2 + p3) * 2 - p2
        self.assertEqual(result, expected)

    def test_evaluate_complex_polynomial(self):
        """Test obliczania wartości złożonego wielomianu."""
        # Tworzymy wielomian: x^5 - 3x^3 + 2
        p = Polynomial([1, 0, -3, 0, 0, 2])

        # Dla x = 2: 2^5 - 3*2^3 + 2 = 32 - 24 + 2 = 10
        self.assertEqual(p.evaluate(2), 10)

        # Dla x = -1: (-1)^5 - 3*(-1)^3 + 2 = -1 + 3 + 2 = 4
        self.assertEqual(p.evaluate(-1), 4)

    def test_repr(self):
        """Test metody __repr__."""
        p = Polynomial([3, 2, 1])
        self.assertEqual(repr(p), "Polynomial([3, 2, 1])")


if __name__ == "__main__":
    unittest.main()
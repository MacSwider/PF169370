from src.TemperatureConverter import *
import unittest

class TestTemperatureConverter(unittest.TestCase):
    def setUp(self):
        self.converter = TemperatureConverter()

    def test_celsius_to_fahrenheit(self):
        self.assertAlmostEqual(self.converter.celsius_to_fahrenheit(0), 32)
        self.assertAlmostEqual(self.converter.celsius_to_fahrenheit(100), 212)
        self.assertAlmostEqual(self.converter.celsius_to_fahrenheit(-273.15), -459.67)

    def test_fahrenheit_to_celsius(self):
        self.assertAlmostEqual(self.converter.fahrenheit_to_celsius(68), 20)
        self.assertAlmostEqual(self.converter.fahrenheit_to_celsius(14), -10)
        self.assertAlmostEqual(self.converter.fahrenheit_to_celsius(122), 50)

    def test_celsius_to_kelvin(self):
        self.assertAlmostEqual(self.converter.celsius_to_kelvin(0), 273.15)
        self.assertAlmostEqual(self.converter.celsius_to_kelvin(-273.15), 0)
        self.assertAlmostEqual(self.converter.celsius_to_kelvin(100), 373.15)

    def test_kelvin_to_celsius(self):
        self.assertAlmostEqual(self.converter.kelvin_to_celsius(273.15), 0)
        self.assertAlmostEqual(self.converter.kelvin_to_celsius(0), -273.15)
        self.assertAlmostEqual(self.converter.kelvin_to_celsius(373.15), 100)


if __name__ == "__main__":
    unittest.main()

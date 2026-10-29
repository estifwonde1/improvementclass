import unittest

from grade_manger import (
    Student,
    calculate_average,
    format_results,
    letter_grade,
    validate_mark,
    validate_name,
)


class TestValidation(unittest.TestCase):
    def test_valid_marks(self):
        self.assertEqual(validate_mark("85"), 85.0)
        self.assertEqual(validate_mark(0), 0.0)
        self.assertEqual(validate_mark("100"), 100.0)

    def test_non_numeric(self):
        for bad in ("abc", "", None, "nan", "inf"):
            with self.assertRaises(ValueError):
                validate_mark(bad)

    def test_out_of_range(self):
        for bad in (-1, "100.1", 150):
            with self.assertRaises(ValueError):
                validate_mark(bad)

    def test_name(self):
        self.assertEqual(validate_name("  Abebe "), "Abebe")
        with self.assertRaises(ValueError):
            validate_name("   ")


class TestCalculations(unittest.TestCase):
    def test_average(self):
        self.assertAlmostEqual(calculate_average([80, 90, 100]), 90.0)
        self.assertAlmostEqual(calculate_average([70]), 70.0)

    def test_average_empty(self):
        with self.assertRaises(ValueError):
            calculate_average([])

    def test_letter_boundaries(self):
        cases = {100: "A", 90: "A", 89.99: "B", 80: "B", 79.99: "C",
                 70: "C", 69.99: "D", 60: "D", 59.99: "F", 0: "F"}
        for avg, expected in cases.items():
            self.assertEqual(letter_grade(avg), expected, avg)

    def test_letter_out_of_range(self):
        with self.assertRaises(ValueError):
            letter_grade(101)


class TestDisplay(unittest.TestCase):
    def test_empty(self):
        self.assertIn("No students", format_results([]))

    def test_table(self):
        out = format_results([Student("Sara", [90, 95]), Student("Dawit", [50])])
        self.assertIn("Sara", out)
        self.assertIn("92.50", out)
        self.assertIn("F", out)


if __name__ == "__main__":
    unittest.main()
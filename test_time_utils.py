import unittest
from datetime import datetime

from time_utils import calculate_diff, calculate_overtime, format_hours


def time(value):
    return datetime.strptime(value, "%I:%M %p")


class TimeUtilsTests(unittest.TestCase):
    def test_existing_net_hours(self):
        self.assertEqual(calculate_diff(time("9:00 AM"), time("6:15 PM")), (555.0, 525.0, 8.75))

    def test_existing_net_hours_overnight(self):
        self.assertEqual(calculate_diff(time("10:00 PM"), time("6:00 AM")), (480.0, 450.0, 7.5))

    def test_zero_overtime(self):
        self.assertEqual(calculate_overtime(time("9:00 AM"), time("6:15 PM"), time("6:15 PM")), 0)

    def test_positive_overtime(self):
        self.assertEqual(calculate_overtime(time("9:00 AM"), time("6:15 PM"), time("7:00 PM")), 45)

    def test_early_finish_has_no_overtime(self):
        self.assertEqual(calculate_overtime(time("9:00 AM"), time("6:15 PM"), time("5:30 PM")), 0)

    def test_overtime_after_midnight(self):
        self.assertEqual(calculate_overtime(time("9:00 AM"), time("6:15 PM"), time("1:00 AM")), 405)

    def test_overnight_schedule(self):
        self.assertEqual(calculate_overtime(time("10:00 PM"), time("6:00 AM"), time("7:00 AM")), 60)

    def test_hour_format_preserves_quarters(self):
        self.assertEqual(format_hours(8.75), "8.75")
        self.assertEqual(format_hours(9.5), "9.5")
        self.assertEqual(format_hours(10.0), "10")


if __name__ == "__main__":
    unittest.main()

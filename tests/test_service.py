"""Unit tests for the gradebook service module."""

from __future__ import annotations

import unittest
from unittest.mock import patch

from gradebook.service import add_course, add_grade, add_student, compute_average


class GradebookServiceTests(unittest.TestCase):
    """Test the gradebook service logic."""

    def setUp(self):
        self.data = {"students": [], "courses": [], "enrollments": []}

    def test_add_student_happy_path(self):
        with patch("gradebook.service.load_data", return_value=self.data), patch(
            "gradebook.service.save_data", side_effect=lambda payload: self.data.update(payload)
        ):
            student_id = add_student("Alice")
            self.assertEqual(student_id, 1)
            self.assertEqual(self.data["students"][0]["name"], "Alice")

    def test_add_grade_happy_path(self):
        self.data["students"] = [{"id": 1, "name": "Alice"}]
        self.data["courses"] = [{"code": "CS101", "title": "Intro to CS"}]
        self.data["enrollments"] = [{"student_id": 1, "course_code": "CS101", "grades": [80]}]

        with patch("gradebook.service.load_data", return_value=self.data), patch(
            "gradebook.service.save_data", side_effect=lambda payload: self.data.update(payload)
        ):
            result = add_grade(1, "CS101", 90)
            self.assertEqual(result, 90.0)
            self.assertEqual(self.data["enrollments"][0]["grades"], [80, 90.0])

    def test_compute_average_happy_path(self):
        self.data["enrollments"] = [{"student_id": 1, "course_code": "CS101", "grades": [90, 80, 100]}]

        with patch("gradebook.service.load_data", return_value=self.data), patch(
            "gradebook.service.save_data", side_effect=lambda payload: self.data.update(payload)
        ):
            average = compute_average(1, "CS101")
            self.assertAlmostEqual(average, 90.0)

    def test_add_grade_rejects_invalid_grade(self):
        self.data["enrollments"] = [{"student_id": 1, "course_code": "CS101", "grades": []}]

        with patch("gradebook.service.load_data", return_value=self.data), patch(
            "gradebook.service.save_data", side_effect=lambda payload: self.data.update(payload)
        ):
            with self.assertRaises(ValueError):
                add_grade(1, "CS101", 101)


if __name__ == "__main__":
    unittest.main()

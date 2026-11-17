"""Seed the gradebook with sample data."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from gradebook.service import add_course, add_grade, add_student, enroll


def seed() -> None:
    """Populate the default data file with sample students, courses, and grades."""
    from gradebook.storage import save_data

    save_data({"students": [], "courses": [], "enrollments": []})

    student_ids = [
        add_student("Alice Johnson"),
        add_student("Bob Smith"),
        add_student("Carol Lee"),
    ]
    add_course("CS101", "Intro to CS")
    add_course("MATH200", "Discrete Math")

    enroll(student_ids[0], "CS101")
    enroll(student_ids[0], "MATH200")
    enroll(student_ids[1], "CS101")
    enroll(student_ids[2], "MATH200")

    add_grade(student_ids[0], "CS101", 95)
    add_grade(student_ids[0], "CS101", 88)
    add_grade(student_ids[0], "MATH200", 92)
    add_grade(student_ids[1], "CS101", 80)
    add_grade(student_ids[2], "MATH200", 76)

    print("Sample gradebook seeded successfully.")


if __name__ == "__main__":
    seed()

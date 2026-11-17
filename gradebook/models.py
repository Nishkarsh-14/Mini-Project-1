"""Domain models for the gradebook application."""

from __future__ import annotations


class Student:
    """Represents a student enrolled in the gradebook."""

    def __init__(self, student_id: int, name: str):
        if not isinstance(student_id, int) or student_id <= 0:
            raise ValueError("Student ID must be a positive integer.")
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Student name cannot be empty.")

        self.id = student_id
        self.name = name.strip()

    def __str__(self) -> str:
        return f"Student(id={self.id}, name='{self.name}')"


class Course:
    """Represents a course offered by the school."""

    def __init__(self, code: str, title: str):
        if not isinstance(code, str) or not code.strip():
            raise ValueError("Course code cannot be empty.")
        if not isinstance(title, str) or not title.strip():
            raise ValueError("Course title cannot be empty.")

        self.code = code.strip().upper()
        self.title = title.strip()

    def __str__(self) -> str:
        return f"Course(code='{self.code}', title='{self.title}')"


class Enrollment:
    """Represents a student's enrollment in a course with a list of grades."""

    def __init__(self, student_id: int, course_code: str, grades: list[int | float] | None = None):
        if not isinstance(student_id, int) or student_id <= 0:
            raise ValueError("Student ID must be a positive integer.")
        if not isinstance(course_code, str) or not course_code.strip():
            raise ValueError("Course code cannot be empty.")

        self.student_id = student_id
        self.course_code = course_code.strip().upper()
        self.grades = [] if grades is None else list(grades)

        for grade in self.grades:
            if not isinstance(grade, (int, float)) or not 0 <= grade <= 100:
                raise ValueError("Each grade must be a number between 0 and 100.")

    def __str__(self) -> str:
        return (
            f"Enrollment(student_id={self.student_id}, "
            f"course_code='{self.course_code}', grades={self.grades})"
        )

"""Business logic for the gradebook application."""

from __future__ import annotations

from typing import Any

from .models import Course, Enrollment, Student
from .storage import load_data, save_data


def parse_grade(value: Any) -> float:
    """Convert a grade input to a float between 0 and 100."""
    try:
        grade = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError("Grade must be a numeric value between 0 and 100.") from exc

    if not 0 <= grade <= 100:
        raise ValueError("Grade must be between 0 and 100.")

    return grade


def _sorted_students(students: list[dict[str, Any]], sort_key: str = "name") -> list[dict[str, Any]]:
    """Sort students using a specified key."""
    return sorted(students, key=lambda student: student[sort_key].lower() if isinstance(student[sort_key], str) else student[sort_key])


def _sorted_courses(courses: list[dict[str, Any]], sort_key: str = "code") -> list[dict[str, Any]]:
    """Sort courses using a specified key."""
    return sorted(courses, key=lambda course: course[sort_key].lower() if isinstance(course[sort_key], str) else course[sort_key])


def add_student(name: str) -> int:
    """Create a new student and save it to the data store."""
    clean_name = name.strip()
    if not clean_name:
        raise ValueError("Student name cannot be empty.")

    data = load_data()
    students = data.get("students", [])
    next_id = max((student["id"] for student in students), default=0) + 1
    student = Student(next_id, clean_name)

    students.append({"id": student.id, "name": student.name})
    data["students"] = students
    save_data(data)
    return student.id


def add_course(code: str, title: str) -> str:
    """Create a new course and save it to the data store."""
    clean_code = code.strip().upper()
    clean_title = title.strip()
    if not clean_code or not clean_title:
        raise ValueError("Course code and title cannot be empty.")

    data = load_data()
    courses = data.get("courses", [])
    if any(existing["code"].lower() == clean_code.lower() for existing in courses):
        raise ValueError(f"Course '{clean_code}' already exists.")

    course = Course(clean_code, clean_title)
    courses.append({"code": course.code, "title": course.title})
    data["courses"] = courses
    save_data(data)
    return course.code


def enroll(student_id: int, course_code: str) -> dict[str, Any]:
    """Enroll a student in a course and persist the change."""
    data = load_data()
    students = data.get("students", [])
    courses = data.get("courses", [])
    enrollments = data.get("enrollments", [])

    if not any(student["id"] == student_id for student in students):
        raise ValueError(f"Unknown student ID: {student_id}")
    if not any(course["code"].lower() == course_code.strip().upper().lower() for course in courses):
        raise ValueError(f"Unknown course code: {course_code}")
    if any(
        enrollment["student_id"] == student_id and enrollment["course_code"].lower() == course_code.strip().upper().lower()
        for enrollment in enrollments
    ):
        raise ValueError(f"Student {student_id} is already enrolled in {course_code}.")

    enrollment = Enrollment(student_id, course_code.strip().upper())
    enrollments.append({
        "student_id": enrollment.student_id,
        "course_code": enrollment.course_code,
        "grades": enrollment.grades,
    })
    data["enrollments"] = enrollments
    save_data(data)
    return {"student_id": enrollment.student_id, "course_code": enrollment.course_code, "grades": enrollment.grades}


def add_grade(student_id: int, course_code: str, grade: Any) -> float:
    """Add a grade to an existing enrollment."""
    numeric_grade = parse_grade(grade)
    data = load_data()
    enrollments = data.get("enrollments", [])

    for enrollment in enrollments:
        if enrollment["student_id"] == student_id and enrollment["course_code"].lower() == course_code.strip().upper().lower():
            enrollment["grades"].append(numeric_grade)
            save_data(data)
            return numeric_grade

    raise ValueError(f"Student {student_id} is not enrolled in {course_code}.")


def list_students(sort_by: str = "name") -> list[dict[str, Any]]:
    """Return a sorted list of students."""
    data = load_data()
    students = data.get("students", [])
    return _sorted_students(students, sort_key=sort_by if sort_by in {"name", "id"} else "name")


def list_courses(sort_by: str = "code") -> list[dict[str, Any]]:
    """Return a sorted list of courses."""
    data = load_data()
    courses = data.get("courses", [])
    return _sorted_courses(courses, sort_key=sort_by if sort_by in {"code", "title"} else "code")


def list_enrollments(sort_by: str = "student_id") -> list[dict[str, Any]]:
    """Return a sorted list of enrollments."""
    data = load_data()
    enrollments = data.get("enrollments", [])
    if not enrollments:
        return []
    return sorted(enrollments, key=lambda item: (item.get(sort_by, 0), str(item.get("course_code", "")).lower()))


def compute_average(student_id: int, course_code: str) -> float:
    """Compute the average grade for a single student/course pair."""
    data = load_data()
    enrollments = data.get("enrollments", [])
    for enrollment in enrollments:
        if enrollment["student_id"] == student_id and enrollment["course_code"].lower() == course_code.strip().upper().lower():
            if not enrollment["grades"]:
                raise ValueError(f"No grades recorded for student {student_id} in {course_code}.")
            return sum(enrollment["grades"]) / len(enrollment["grades"])

    raise ValueError(f"Student {student_id} is not enrolled in {course_code}.")


def compute_gpa(student_id: int) -> float:
    """Compute the simple mean of a student's course averages."""
    data = load_data()
    student_exists = any(student["id"] == student_id for student in data.get("students", []))
    if not student_exists:
        raise ValueError(f"Unknown student ID: {student_id}")

    enrollments = [
        enrollment for enrollment in data.get("enrollments", []) if enrollment["student_id"] == student_id
    ]
    if not enrollments:
        return 0.0

    course_averages = [
        sum(enrollment["grades"]) / len(enrollment["grades"]) for enrollment in enrollments if enrollment["grades"]
    ]
    if not course_averages:
        return 0.0
    return sum(course_averages) / len(course_averages)

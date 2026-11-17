"""Command-line interface for the gradebook application."""

from __future__ import annotations

import argparse
import logging
import sys

from gradebook.service import (
    add_course,
    add_grade,
    add_student,
    compute_average,
    compute_gpa,
    enroll,
    list_courses,
    list_enrollments,
    list_students,
)

logger = logging.getLogger("gradebook")
logger.setLevel(logging.INFO)
if not logger.handlers:
    from pathlib import Path

    log_path = Path(__file__).resolve().parent / "logs" / "app.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    handler = logging.FileHandler(log_path)
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(handler)


def print_students(rows: list[dict[str, object]]) -> None:
    """Display all students in a readable format."""
    if not rows:
        print("No students found.")
        return
    for student in rows:
        print(f"Student {student['id']}: {student['name']}")


def print_courses(rows: list[dict[str, object]]) -> None:
    """Display all courses in a readable format."""
    if not rows:
        print("No courses found.")
        return
    for course in rows:
        print(f"{course['code']}: {course['title']}")


def print_enrollments(rows: list[dict[str, object]]) -> None:
    """Display all enrollments in a readable format."""
    if not rows:
        print("No enrollments found.")
        return
    for item in rows:
        grades = item.get("grades", [])
        grades_text = ", ".join(str(grade) for grade in grades) if grades else "No grades"
        print(f"Student {item['student_id']} -> {item['course_code']} [{grades_text}]")


def build_parser() -> argparse.ArgumentParser:
    """Create the argument parser for the CLI."""
    parser = argparse.ArgumentParser(description="Gradebook CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_student_parser = subparsers.add_parser("add-student", help="Add a student")
    add_student_parser.add_argument("--name", required=True, help="Student name")

    add_course_parser = subparsers.add_parser("add-course", help="Add a course")
    add_course_parser.add_argument("--code", required=True, help="Course code")
    add_course_parser.add_argument("--title", required=True, help="Course title")

    enroll_parser = subparsers.add_parser("enroll", help="Enroll student in a course")
    enroll_parser.add_argument("--student-id", type=int, required=True)
    enroll_parser.add_argument("--course", required=True)

    add_grade_parser = subparsers.add_parser("add-grade", help="Add a grade")
    add_grade_parser.add_argument("--student-id", type=int, required=True)
    add_grade_parser.add_argument("--course", required=True)
    add_grade_parser.add_argument("--grade", required=True)

    list_parser = subparsers.add_parser("list", help="List students, courses, or enrollments")
    list_parser.add_argument("entity", choices=["students", "courses", "enrollments"])
    list_parser.add_argument("--sort", default=None)

    avg_parser = subparsers.add_parser("avg", help="Get average score for a course")
    avg_parser.add_argument("--student-id", type=int, required=True)
    avg_parser.add_argument("--course", required=True)

    gpa_parser = subparsers.add_parser("gpa", help="Get GPA for a student")
    gpa_parser.add_argument("--student-id", type=int, required=True)

    return parser


def main() -> int:
    """Run the CLI command dispatcher."""
    parser = build_parser()
    args = parser.parse_args()

    try:
        if args.command == "add-student":
            student_id = add_student(args.name)
            print(f"Student added with ID {student_id}.")
        elif args.command == "add-course":
            course_code = add_course(args.code, args.title)
            print(f"Course {course_code} added.")
        elif args.command == "enroll":
            result = enroll(args.student_id, args.course)
            print(f"Student {result['student_id']} enrolled in {result['course_code']}.")
        elif args.command == "add-grade":
            result = add_grade(args.student_id, args.course, args.grade)
            print(f"Grade {result} added for student {args.student_id} in {args.course}.")
        elif args.command == "list":
            sort_key = args.sort
            if args.entity == "students":
                sort_key = sort_key or "name"
                print_students(list_students(sort_by=sort_key))
            elif args.entity == "courses":
                sort_key = sort_key or "code"
                print_courses(list_courses(sort_by=sort_key))
            else:
                sort_key = sort_key or "student_id"
                print_enrollments(list_enrollments(sort_by=sort_key))
        elif args.command == "avg":
            average = compute_average(args.student_id, args.course)
            print(f"Average for student {args.student_id} in {args.course}: {average:.2f}")
        elif args.command == "gpa":
            average = compute_gpa(args.student_id)
            print(f"GPA for student {args.student_id}: {average:.2f}")
        else:
            parser.error("Unknown command.")
        return 0
    except (TypeError, ValueError) as exc:
        logger.error("CLI error: %s", exc)
        print(f"Error: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

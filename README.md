# Gradebook CLI

A small Python command-line gradebook application built with standard-library modules only.

## Setup

1. Open a terminal in the project root.
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```
3. Install nothing extra because the project uses the Python standard library.

## Seed sample data

Run the sample data generator to create 2-3 students, a pair of courses, and grade entries:

```bash
python scripts/seed.py
```

This saves data to `data/gradebook.json`.

## Example CLI commands

```bash
python main.py add-student --name "Alice Johnson"
python main.py add-course --code CS101 --title "Intro to CS"
python main.py enroll --student-id 1 --course CS101
python main.py add-grade --student-id 1 --course CS101 --grade 95
python main.py list students --sort name
python main.py list courses --sort code
python main.py list enrollments --sort student_id
python main.py avg --student-id 1 --course CS101
python main.py gpa --student-id 1
```

Example expected output:

```text
Student added with ID 1.
Course CS101 added.
Student 1 enrolled in CS101.
Grade 95.0 added for student 1 in CS101.
Student 1: Alice Johnson
CS101: Intro to CS
Student 1 -> CS101 [95.0]
Average for student 1 in CS101: 95.00
GPA for student 1: 95.00
```

## Running tests

```bash
python -m unittest discover -s tests
```

## Design decisions & limitations

- Data is stored in a single JSON file for simplicity.
- There is no database or authentication layer; this is a local, single-user CLI app.
- GPA is calculated as the mean of each course average for a student.
- Validation is intentionally lightweight and focused on common user-input errors.

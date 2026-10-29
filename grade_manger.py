"""Student Grade Management System.

Accepts student marks, validates them, calculates the average and a
letter grade, and displays the results.
"""

from dataclasses import dataclass, field

MIN_MARK = 0.0
MAX_MARK = 100.0

# (minimum average, letter) checked from highest to lowest.
GRADE_SCALE = [(90, "A"), (80, "B"), (70, "C"), (60, "D")]
FAIL_GRADE = "F"


@dataclass
class Student:
    name: str
    marks: list = field(default_factory=list)

    @property
    def average(self) -> float:
        return calculate_average(self.marks)

    @property
    def grade(self) -> str:
        return letter_grade(self.average)


def validate_name(name: str) -> str:
    """Return a cleaned name or raise ValueError if it is empty."""
    cleaned = name.strip()
    if not cleaned:
        raise ValueError("Name cannot be empty.")
    return cleaned


def validate_mark(raw) -> float:
    """Convert raw input to a float mark in [0, 100] or raise ValueError."""
    try:
        mark = float(raw)
    except (TypeError, ValueError):
        raise ValueError(f"'{raw}' is not a number.")
    if mark != mark or mark in (float("inf"), float("-inf")):
        raise ValueError("Mark must be a finite number.")
    if not MIN_MARK <= mark <= MAX_MARK:
        raise ValueError(f"Mark must be between {MIN_MARK:g} and {MAX_MARK:g}.")
    return mark


def calculate_average(marks) -> float:
    """Return the mean of the marks. Raises ValueError if there are none."""
    if not marks:
        raise ValueError("At least one mark is required.")
    return sum(marks) / len(marks)


def letter_grade(average: float) -> str:
    """Map an average to a letter grade."""
    if not MIN_MARK <= average <= MAX_MARK:
        raise ValueError("Average out of range.")
    for threshold, letter in GRADE_SCALE:
        if average >= threshold:
            return letter
    return FAIL_GRADE


def read_student() -> Student:
    """Prompt for a student's name and marks, re-asking on invalid input."""
    while True:
        try:
            name = validate_name(input("Student name: "))
            break
        except ValueError as err:
            print(f"  Invalid: {err}")

    while True:
        try:
            count = int(input("Number of subjects: "))
            if count < 1:
                raise ValueError
            break
        except ValueError:
            print("  Invalid: enter a whole number of 1 or more.")

    marks = []
    for i in range(1, count + 1):
        while True:
            try:
                marks.append(validate_mark(input(f"  Mark {i} (0-100): ")))
                break
            except ValueError as err:
                print(f"  Invalid: {err}")
    return Student(name, marks)


def format_results(students) -> str:
    """Build a text table of all students' results."""
    if not students:
        return "No students recorded yet."
    width = max(len("Name"), *(len(s.name) for s in students))
    header = f"{'Name':<{width}}  {'Subjects':>8}  {'Average':>7}  Grade"
    lines = [header, "-" * len(header)]
    for s in students:
        lines.append(
            f"{s.name:<{width}}  {len(s.marks):>8}  {s.average:>7.2f}  {s.grade}"
        )
    return "\n".join(lines)


def main() -> None:
    students = []
    menu = "\n1) Add student  2) Show results  3) Quit\nChoose: "
    while True:
        choice = input(menu).strip()
        if choice == "1":
            students.append(read_student())
        elif choice == "2":
            print("\n" + format_results(students))
        elif choice == "3":
            print("Goodbye.")
            break
        else:
            print("Please choose 1, 2, or 3.")


if __name__ == "__main__":
    main()
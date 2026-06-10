from students.validation import validate_id
from students.validation import validate_name

STUDENT_FILE = "data/students.txt"


def add_student():
    student_id = input("Enter Student ID: ")
    name = input("Enter Student Name: ")

    if not validate_id(student_id):
        print("Invalid ID")
        return

    if not validate_name(name):
        print("Invalid Name")
        return

    with open(STUDENT_FILE, "a") as file:
        file.write(f"{student_id},{name}\n")

    print("Student Added Successfully")


def view_students():
    try:
        with open(STUDENT_FILE, "r") as file:
            students = file.readlines()

        print("\n===== STUDENTS =====")

        for student in students:
            print(student.strip())

    except FileNotFoundError:
        print("No students found.")
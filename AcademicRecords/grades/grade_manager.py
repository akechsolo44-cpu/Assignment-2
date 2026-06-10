GRADE_FILE = "data/grades.txt"


def add_grade():
    student_id = input("Student ID: ")
    course_id = input("Course ID: ")
    grade = input("Grade: ")

    with open(GRADE_FILE, "a") as file:
        file.write(f"{student_id},{course_id},{grade}\n")

    print("Grade Added Successfully")


def view_grades():
    try:
        with open(GRADE_FILE, "r") as file:
            grades = file.readlines()

        print("\n===== GRADES =====")

        for grade in grades:
            print(grade.strip())

    except FileNotFoundError:
        print("No grades found.")
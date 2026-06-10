from students.student_manager import add_student, view_students
from courses.course_manager import add_course, view_courses
from grades.grade_manager import add_grade, view_grades
from reports.report_generator import generate_report


while True:

    print("\n===== ACADEMIC RECORD SYSTEM =====")
    print("1. Add Student")
    print("2. View Students")
    print("3. Add Course")
    print("4. View Courses")
    print("5. Add Grade")
    print("6. View Grades")
    print("7. Generate Report")
    print("8. Exit")

    choice = input("Choose an option: ")

    if choice == "1":
        add_student()

    elif choice == "2":
        view_students()

    elif choice == "3":
        add_course()

    elif choice == "4":
        view_courses()

    elif choice == "5":
        add_grade()

    elif choice == "6":
        view_grades()

    elif choice == "7":
        generate_report()

    elif choice == "8":
        print("Goodbye!")
        break

    else:
        print("Invalid choice.")
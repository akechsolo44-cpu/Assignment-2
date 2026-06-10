def generate_report():

    print("\n===== ACADEMIC REPORT =====")

    try:
        print("\nStudents")
        with open("data/students.txt", "r") as file:
            print(file.read())
    except:
        print("No student records.")

    try:
        print("\nCourses")
        with open("data/courses.txt", "r") as file:
            print(file.read())
    except:
        print("No course records.")

    try:
        print("\nGrades")
        with open("data/grades.txt", "r") as file:
            print(file.read())
    except:
        print("No grade records.")
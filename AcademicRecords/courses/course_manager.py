COURSE_FILE = "data/courses.txt"


def add_course():
    course_id = input("Enter Course ID: ")
    course_name = input("Enter Course Name: ")

    with open(COURSE_FILE, "a") as file:
        file.write(f"{course_id},{course_name}\n")

    print("Course Added Successfully")


def view_courses():
    try:
        with open(COURSE_FILE, "r") as file:
            courses = file.readlines()

        print("\n===== COURSES =====")

        for course in courses:
            print(course.strip())

    except FileNotFoundError:
        print("No courses found.")
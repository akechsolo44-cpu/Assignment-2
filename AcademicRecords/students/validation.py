def validate_id(student_id):
    return student_id.isdigit()

def validate_name(name):
    return len(name.strip()) > 0
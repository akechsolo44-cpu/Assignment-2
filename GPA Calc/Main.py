import pandas as pd

subjects = pd.DataFrame({
    "SubjectCode": ["IF101", "IF102", "IF103"],
    "SubjectName": [
        "Programming Fundamentals",
        "Database Systems",
        "Web Programming"
    ],
    "SKS": [3, 3, 2]
})

students = pd.DataFrame({
    "StudentID": ["S001", "S002", "S003"],
    "StudentName": ["Machar", "Deng", "Akech"],
    "Group": ["A", "A", "B"]
})

scores = pd.DataFrame({
    "ID": [1, 2, 3, 4],
    "SubjectCode": ["IF101", "IF102", "IF101", "IF103"],
    "StudentID": ["S001", "S001", "S002", "S003"],
    "Score": [85, 78, 90, 88]
})

with pd.ExcelWriter("AcademicData.xlsx") as writer:
    subjects.to_excel(writer, sheet_name="Subjects", index=False)
    students.to_excel(writer, sheet_name="Students", index=False)
    scores.to_excel(writer, sheet_name="RawScores", index=False)

print("Workbook created successfully!")

import pandas as pd

xls = pd.ExcelFile("AcademicData.xlsx")
print(xls.sheet_names)

import pandas as pd

file_name = "AcademicData.xlsx"

subjects_df = pd.read_excel(file_name, sheet_name="Subjects")
students_df = pd.read_excel(file_name, sheet_name="Students")
scores_df = pd.read_excel(file_name, sheet_name="RawScores")

print("Subjects")
print(subjects_df)

print("\nStudents")
print(students_df)

print("\nScores")
print(scores_df)

merged_df = scores_df.merge(
    students_df,
    on="StudentID",
    how="left"
)

merged_df = merged_df.merge(
    subjects_df,
    on="SubjectCode",
    how="left"
)

print("\nMerged Data")
print(merged_df)

def get_grade(score):
    if score >= 85:
        return "A"
    elif score >= 70:
        return "B"
    elif score >= 55:
        return "C"
    elif score >= 40:
        return "D"
    else:
        return "E"
    
merged_df["Grade"] = merged_df["Score"].apply(get_grade)

grade_points = {
    "A": 4,
    "B": 3,
    "C": 2,
    "D": 1,
    "E": 0
}

merged_df["Point"] = merged_df["Grade"].map(grade_points)

merged_df["WeightedPoint"] = (
    merged_df["Point"] * merged_df["SKS"]
)

gpa_report = merged_df.groupby(
    ["StudentID", "StudentName"]
).agg(
    TotalSKS=("SKS", "sum"),
    TotalWeightedPoints=("WeightedPoint", "sum")
).reset_index()

gpa_report["GPA"] = (
    gpa_report["TotalWeightedPoints"]
    / gpa_report["TotalSKS"]
)

gpa_report["GPA"] = gpa_report["GPA"].round(2)

average_gpa = gpa_report["GPA"].mean()

print("\nAverage GPA:", round(average_gpa, 2))

with pd.ExcelWriter(
    file_name,
    engine="openpyxl",
    mode="a",
    if_sheet_exists="replace"
) as writer:

    gpa_report.to_excel(
        writer,
        sheet_name="GPA_Report",
        index=False
    )
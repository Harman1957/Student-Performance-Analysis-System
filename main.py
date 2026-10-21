"""
Student Performance Analysis System
Mini project using Python, Pandas and Matplotlib.
Run: python main.py
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "students.csv"
OUTPUT_DIR = BASE_DIR / "outputs"
SUBJECTS = ["English", "Mathematics", "Science", "Computer", "Social_Studies"]
PASS_MARK = 40
MAX_MARKS = 100

def load_data():
    """Load and validate the student dataset."""
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Dataset not found: {DATA_FILE}")
    df = pd.read_csv(DATA_FILE)
    required = ["Student_ID", "Name"] + SUBJECTS
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")
    for subject in SUBJECTS:
        df[subject] = pd.to_numeric(df[subject], errors="raise")
        if ((df[subject] < 0) | (df[subject] > MAX_MARKS)).any():
            raise ValueError(f"Marks in {subject} must be between 0 and 100.")
    if df["Student_ID"].duplicated().any():
        raise ValueError("Student_ID values must be unique.")
    return df

def analyze_data(df):
    """Add total, percentage, grade, pass/fail and support flag."""
    result = df.copy()
    result["Total"] = result[SUBJECTS].sum(axis=1)
    result["Percentage"] = (result["Total"] / (len(SUBJECTS) * MAX_MARKS) * 100).round(2)
    result["Grade"] = result["Percentage"].apply(get_grade)
    result["Result"] = result[SUBJECTS].ge(PASS_MARK).all(axis=1).map(
        {True: "Pass", False: "Needs Improvement"}
    )
    result["Support_Subjects"] = result.apply(
        lambda row: ", ".join([s for s in SUBJECTS if row[s] < PASS_MARK]) or "None",
        axis=1
    )
    return result

def get_grade(percentage):
    if percentage >= 90:
        return "A+"
    if percentage >= 80:
        return "A"
    if percentage >= 70:
        return "B"
    if percentage >= 60:
        return "C"
    if percentage >= 50:
        return "D"
    if percentage >= 40:
        return "E"
    return "F"

def show_summary(result):
    total_students = len(result)
    passed = int((result["Result"] == "Pass").sum())
    needs_help = total_students - passed
    average = result["Percentage"].mean()
    print("\n" + "=" * 64)
    print("          STUDENT PERFORMANCE ANALYSIS SYSTEM")
    print("=" * 64)
    print(f"Students analyzed       : {total_students}")
    print(f"Class average           : {average:.2f}%")
    print(f"Passed all subjects     : {passed}")
    print(f"Need improvement       : {needs_help}")
    print(f"Class pass percentage   : {(passed / total_students * 100 if total_students else 0):.2f}%")
    print("-" * 64)

def show_all_students(result):
    columns = ["Student_ID", "Name", "Total", "Percentage", "Grade", "Result"]
    print("\nSTUDENT RESULTS")
    print(result[columns].to_string(index=False))

def show_subject_analysis(df):
    print("\nSUBJECT-WISE CLASS ANALYSIS")
    summary = pd.DataFrame({
        "Subject": SUBJECTS,
        "Average Marks": [round(df[s].mean(), 2) for s in SUBJECTS],
        "Highest Marks": [int(df[s].max()) for s in SUBJECTS],
        "Lowest Marks": [int(df[s].min()) for s in SUBJECTS],
        "Students Below 40": [int((df[s] < PASS_MARK).sum()) for s in SUBJECTS],
    })
    print(summary.to_string(index=False))
    return summary

def save_outputs(result, subject_summary):
    OUTPUT_DIR.mkdir(exist_ok=True)
    result.to_csv(OUTPUT_DIR / "student_analysis_results.csv", index=False)
    subject_summary.to_csv(OUTPUT_DIR / "subject_summary.csv", index=False)

    # Chart 1: average marks by subject
    averages = [result[s].mean() for s in SUBJECTS]
    plt.figure(figsize=(9, 5))
    plt.bar(SUBJECTS, averages)
    plt.title("Average Marks by Subject")
    plt.xlabel("Subject")
    plt.ylabel("Average Marks (out of 100)")
    plt.ylim(0, 100)
    plt.xticks(rotation=20, ha="right")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "subject_average.png", dpi=150)
    plt.close()

    # Chart 2: percentage per student
    plt.figure(figsize=(10, 5))
    plt.bar(result["Name"], result["Percentage"])
    plt.title("Student Percentage Comparison")
    plt.xlabel("Student")
    plt.ylabel("Percentage")
    plt.ylim(0, 100)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "student_percentages.png", dpi=150)
    plt.close()

    # Chart 3: grade distribution
    grade_order = ["A+", "A", "B", "C", "D", "E", "F"]
    counts = result["Grade"].value_counts().reindex(grade_order, fill_value=0)
    plt.figure(figsize=(7, 5))
    plt.pie(counts.values, labels=counts.index, autopct="%1.1f%%", startangle=90)
    plt.title("Grade Distribution")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "grade_distribution.png", dpi=150)
    plt.close()
    print(f"\nFiles saved successfully in: {OUTPUT_DIR}")

def show_top_students(result):
    print("\nTOP 3 STUDENTS")
    print(result.nlargest(min(3, len(result)), "Percentage")[
        ["Student_ID", "Name", "Percentage", "Grade"]
    ].to_string(index=False))

def show_students_for_support(result):
    needs_help = result[result["Result"] == "Needs Improvement"]
    print("\nSTUDENTS WHO MAY NEED EXTRA SUPPORT")
    if needs_help.empty:
        print("No students are below the pass mark in any subject.")
    else:
        print(needs_help[["Student_ID", "Name", "Percentage", "Support_Subjects"]].to_string(index=False))

def main():
    try:
        df = load_data()
        result = analyze_data(df)
        subject_summary = show_subject_analysis(df)
        show_summary(result)
        show_all_students(result)
        show_top_students(result)
        show_students_for_support(result)
        save_outputs(result, subject_summary)
        print("\nAnalysis completed. Open the outputs folder to view CSV files and charts.")
    except (FileNotFoundError, ValueError, pd.errors.ParserError) as error:
        print(f"\nError: {error}")
        print("Please check students.csv and run the program again.")

if __name__ == "__main__":
    main()

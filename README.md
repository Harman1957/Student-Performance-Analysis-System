# Student Performance Analysis System

A Python mini project that analyzes fictional student marks with Pandas and visualizes results with Matplotlib.

## Features
- Calculates total, percentage, and grade.
- Checks pass status across all subjects.
- Lists subjects where marks are below 40.
- Prints class and subject summaries.
- Exports analysis CSV files and saves three charts.

## Requirements
Python 3.10 or later is recommended.

## Setup in VS Code
```bash
python -m venv .venv
```
Windows PowerShell:
```powershell
.venv\Scripts\Activate.ps1
```
Install packages:
```bash
python -m pip install -r requirements.txt
```
Run:
```bash
python main.py
```

## Dataset
`students.csv` contains fictional sample data. Replace it only with data you are authorized to use. The example pass threshold is 40 marks per subject.

## Output
Generated files appear in `outputs/`:
- `student_analysis_results.csv`
- `subject_summary.csv`
- `subject_average.png`
- `student_percentages.png`
- `grade_distribution.png`

## Case study
See `case_study.md`. A Word report should include the actual program output and screenshots from your own run.

## GitHub
Create an empty repository named `Student-Performance-Analysis-System` on GitHub, then push this folder (do not upload your virtual environment).

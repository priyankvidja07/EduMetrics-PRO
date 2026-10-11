# Data Dictionary

This document describes the schema of the student performance dataset used in this project.

**Disclaimer**: The default data (`data/sample_student_performance.csv`) is **100% synthetic** and generated purely for demonstration purposes. It does not reflect any real students or institutional records.

## Schema

| Column Name | Data Type | Description / Valid Range |
|-------------|-----------|---------------------------|
| `student_id` | String | Unique anonymized identifier (e.g., STU001) |
| `student_name` | String | Synthetic student name |
| `semester` | Integer | Academic semester (default 5) |
| `gender` | Category | Male or Female |
| `subject` | Category | Name of the subject (e.g., Data Science) |
| `internal_marks` | Numeric | 0 to 30. Missing values allowed. |
| `external_marks` | Numeric | 0 to 70. Missing values allowed. |
| `total_marks` | Numeric | Calculated as internal + external. (0 - 100) |
| `attendance_pct` | Numeric | 0 to 100 representing attendance percentage. |
| `study_hours` | Numeric | Average daily study hours (0 - 12). |
| `assignment_score` | Numeric | Assignment score out of 100. |
| `result` | Category | "Pass" if total_marks >= 40, else "Fail". "N/A" if marks missing. |

## Missing Value Handling
By default, the application does not impute academic marks. Missing marks are left as missing (`NaN`) and explicitly flagged in the Data Quality report.

## Calculations
- `total_marks`: Simply the sum of `internal_marks` and `external_marks`. If either is missing, `total_marks` is considered missing.
- `result`: Based on the rule `total_marks >= 40`.

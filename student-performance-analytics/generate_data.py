rimport pandas as pd
import numpy as np
import os

def generate_sample_data(filepath="data/sample_student_performance.csv"):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    np.random.seed(42)
    
    num_students = 60
    subjects = ["Data Science", "Python Programming", "Database Management", "Software Engineering", "Computer Networks"]
    
    records = []
    
    for i in range(1, num_students + 1):
        student_id = f"STU{i:03d}"
        student_name = f"Student_{i}"
        gender = np.random.choice(["Male", "Female"])
        semester = 5
        
        # Base aptitude for the student
        aptitude = np.random.normal(0.6, 0.15)
        aptitude = np.clip(aptitude, 0.2, 0.9)
        
        for subject in subjects:
            study_hours = np.clip(np.random.normal(aptitude * 10, 2), 0.5, 12)
            attendance_pct = np.clip(np.random.normal(aptitude * 80 + 20, 10), 40, 100)
            
            # Marks are correlated with aptitude/study hours
            internal_marks = np.clip(np.random.normal(aptitude * 25 + 5, 3), 0, 30)
            external_marks = np.clip(np.random.normal(aptitude * 60 + 10, 8), 0, 70)
            
            # Inject ~2% missing data randomly
            if np.random.rand() < 0.02: internal_marks = np.nan
            if np.random.rand() < 0.02: external_marks = np.nan
            
            total_marks = internal_marks + external_marks if not pd.isna(internal_marks) and not pd.isna(external_marks) else np.nan
            assignment_score = np.clip(np.random.normal(aptitude * 80 + 10, 10), 20, 100)
            
            if pd.isna(total_marks):
                result = "N/A"
            else:
                result = "Pass" if total_marks >= 40 else "Fail"
                
            records.append({
                "student_id": student_id,
                "student_name": student_name,
                "semester": semester,
                "gender": gender,
                "subject": subject,
                "internal_marks": round(internal_marks) if not pd.isna(internal_marks) else np.nan,
                "external_marks": round(external_marks) if not pd.isna(external_marks) else np.nan,
                "total_marks": round(total_marks) if not pd.isna(total_marks) else np.nan,
                "attendance_pct": round(attendance_pct, 1),
                "study_hours": round(study_hours, 1),
                "assignment_score": round(assignment_score),
                "result": result
            })
            
    df = pd.DataFrame(records)
    df.to_csv(filepath, index=False)
    print(f"Sample data generated at {filepath} with {len(df)} records.")

if __name__ == "__main__":
    generate_sample_data()

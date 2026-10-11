# Student Performance Analytics Dashboard

## Project Overview
This project is an interactive Python web dashboard built for the GTU Bachelor of Engineering Semester 5 Data Science subject. It transforms student academic records into understandable statistical summaries and interactive charts using Matplotlib and Seaborn.

## Presented By
- **Student Name:** UBHADIYA HARIKRUSHN DHIRAJLAL
- **Enrollment Number:** 240310116034
- **Institute:** Shantilal Shah Engineering College (SSEC), Bhavnagar
- **Course:** B.E. Semester 5 (Data Science)

## Features
- **Data Upload**: Load custom datasets via CSV or use the bundled synthetic data.
- **Data Quality**: Validates schemas and checks for outliers or duplicates.
- **Statistical Analysis**: Calculates mean, median, quartiles, skewness, and kurtosis.
- **Visualizations**: Dedicated Matplotlib and Seaborn studios for plotting.
- **Interactive Filtering**: Dynamic filtering by subject, marks, and attendance.
- **Exporting**: Download filtered datasets (CSV) and charts (PNG).

## GTU Syllabus Alignment
This project aligns with the GTU Data Science syllabus, particularly:
- **Unit 2 (Python Essentials)**: Pandas for data manipulation, cleaning, and structuring.
- **Unit 3 (Descriptive Analytics)**: Calculation of percentiles, variation, skewness, kurtosis, and varied visualization techniques via Matplotlib and Seaborn.

## Technology Stack
- **Language:** Python 3.11+
- **Framework:** Streamlit
- **Data Manipulation:** Pandas, NumPy
- **Statistics:** SciPy
- **Visualization:** Matplotlib, Seaborn
- **Testing:** Pytest

## Setup and Installation (Windows)

1. **Create and activate a virtual environment:**
```powershell
python -m venv .venv
.venv\Scripts\activate
```

2. **Install dependencies:**
```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

3. **Generate sample data & Run Application:**
```powershell
python generate_data.py
streamlit run app.py
```

## Known Limitations & Privacy
- This dashboard is for local educational use only.
- It does not connect to an external database.
- Please do not upload real dataset files containing sensitive PII (Personally Identifiable Information). Use anonymized IDs.
- The bundled sample data is purely synthetic.

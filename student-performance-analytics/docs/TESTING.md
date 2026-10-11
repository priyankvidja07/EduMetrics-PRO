# Testing Documentation

The project includes an automated testing suite using `pytest` to ensure data validation, statistical calculations, and visualization components function correctly.

## Running Tests
Ensure you are in your activated virtual environment and in the root project folder:

```powershell
pytest tests/ -v
```

## Test Coverage
- `test_data_validation.py`: Tests the validation layer to ensure missing columns, out-of-bounds data, and invalid datasets are flagged correctly.
- `test_statistics.py`: Asserts correct calculation of descriptive statistics (Mean, Median, Skewness, Kurtosis), and proper handling of edge cases (constant columns, empty datasets).
- `test_visualizations.py`: Ensures Matplotlib and Seaborn plotting functions return valid figure objects without raising errors, even when given empty dataframes.

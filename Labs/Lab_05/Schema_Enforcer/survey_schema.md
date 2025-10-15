# Survey Data Schema

## Table: `clean_survey_data`

This table contains student survey information with validated data types after cleaning and type enforcement.

| Column Name | Required Data Type | Brief Description |
| :--- | :--- | :--- |
| `student_id` | `INT` | Unique identifier for the student. |
| `major` | `VARCHAR(50)` | The student's declared academic major or field of study. |
| `GPA` | `FLOAT` | The student's grade point average on a 4.0 scale. |
| `is_cs_major` | `BOOL` | Boolean flag indicating whether the student is a Computer Science major (True) or not (False). |
| `credits_taken` | `FLOAT` | Total number of academic credits the student has completed. |

## Notes

- **Data Source**: `clean_survey_data.csv`
- **Original Source**: `raw_survey_data.csv` (after type validation and cleaning)
- **VARCHAR Sizing Rationale**: 
  - `major`: Set to 50 characters to accommodate long major names like "Electrical and Computer Engineering" (36 chars) with room for expansion
- **Type Conversions Applied**:
  - `is_cs_major`: Converted from string values ('Yes'/'No') to boolean (True/False)
  - `GPA`: Enforced as float64 to handle decimal precision
  - `credits_taken`: Converted from string to float64 for numeric operations
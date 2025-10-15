# Course Catalog Schema

## Table: `clean_course_catalog`

This table contains normalized course catalog information with flattened instructor data. Each row represents one instructor assigned to a course.

| Column Name | Required Data Type | Brief Description |
| :--- | :--- | :--- |
| `name` | `VARCHAR(100)` | Full name of the instructor or teaching assistant. |
| `role` | `VARCHAR(20)` | The instructor's role in the course (e.g., 'Primary', 'TA'). |
| `course_id` | `VARCHAR(20)` | Unique course identifier code (e.g., 'DS2002', 'CS3240'). |
| `title` | `VARCHAR(100)` | Full title/name of the course. |
| `level` | `INT` | Numeric course level indicating difficulty (e.g., 200, 300, 400). |

## Notes

- **Data Source**: `clean_course_catalog.csv`
- **Original Source**: `raw_course_catalog.json` (after normalization)
- **Normalization Details**:
  - Original JSON structure was hierarchical with nested instructor arrays
  - Used `pd.json_normalize()` with `record_path=['instructors']` to flatten
  - Each instructor for a course now appears as a separate row
  - A course with multiple instructors will have multiple rows in this table
- **VARCHAR Sizing Rationale**:
  - `name`: Set to 100 characters to accommodate long full names with middle names/suffixes
  - `role`: Set to 20 characters to accommodate role descriptions like "Primary", "TA", "Co-Instructor"
  - `course_id`: Set to 20 characters for department codes and course numbers with sections
  - `title`: Set to 100 characters for lengthy course titles with subtitles
- **Relationship**: This is a one-to-many relationship where one course can have many instructors

## Example

For a course with 2 instructors, the data would appear as:

| name | role | course_id | title | level |
|------|------|-----------|-------|-------|
| Austin Rivera | Primary | DS2002 | Data Science Systems | 200 |
| Heywood Williams-Tracy | TA | DS2002 | Data Science Systems | 200 |
import csv
import json
import pandas as pd

data = [
    # Headers
    ['student_id', 'major', 'GPA', 'is_cs_major', 'credits_taken'],
    
    # Records with various type issues
    [101, 'Computer Science', 3.8, 'Yes', '45.0'],     
    [102, 'Mathematics', 3, 'No', '38.5'],             
    [103, 'Physics', 3.5, 'Yes', '42.0'],               
    [104, 'Computer Science', 4, 'Yes', '50.5'],       
    [105, 'Engineering', 2.9, 'No', '35.0'],            
    [106, 'Computer Science', 3, 'Yes', '48.0']        
]

with open('raw_survey_data.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(data)

print("Successfully created 'raw_survey_data.csv'")
print(f"Generated {len(data)-1} student records with 5 columns")
print("Data type issues included")

courses = [
    {
        "course_id": "DS2002",
        "section": "001",
        "title": "Data Science Systems",
        "level": 200,
        "instructors": [
            {"name": "Austin Rivera", "role": "Primary"},
            {"name": "Heywood Williams-Tracy", "role": "TA"}
        ]
    },
    {
        "course_id": "CS3240",
        "section": "002",
        "title": "Advanced Software Development",
        "level": 300,
        "instructors": [
            {"name": "Sherriff Mark", "role": "Primary"},
            {"name": "Sarah Johnson", "role": "TA"}
        ]
    },
    {
        "course_id": "STAT3120",
        "section": "001",
        "title": "Introduction to Probability",
        "level": 300,
        "instructors": [
            {"name": "Michael Chen", "role": "Primary"}
        ]
    },
    {
        "course_id": "CS4774",
        "section": "001",
        "title": "Machine Learning",
        "level": 400,
        "instructors": [
            {"name": "David Evans", "role": "Primary"},
            {"name": "Emily Park", "role": "TA"},
            {"name": "James Rodriguez", "role": "TA"}
        ]
    }
]

with open('raw_course_catalog.json', 'w') as jsonfile:
    json.dump(courses, jsonfile, indent=2)

print("\nSuccessfully created 'raw_course_catalog.json'")
print(f"Generated {len(courses)} course records with nested instructor data")


df_survey = pd.read_csv('raw_survey_data.csv')

print("\nOriginal Data Types:")
print(df_survey.dtypes)
print("\nOriginal Data Sample:")
print(df_survey.head())

df_survey['is_cs_major'] = df_survey['is_cs_major'].replace({'Yes': True, 'No': False})

df_survey = df_survey.astype({
    'GPA': 'float64',
    'credits_taken': 'float64'
})

print("\nCleaned Data Types:")
print(df_survey.dtypes)
print("\nCleaned Data Sample:")
print(df_survey.head())

df_survey.to_csv('clean_survey_data.csv', index=False)

print("\nSuccessfully created 'clean_survey_data.csv'")

with open('raw_course_catalog.json', 'r') as jsonfile:
    course_data = json.load(jsonfile)


df_courses = pd.json_normalize(
    course_data,
    record_path=['instructors'],
    meta=['course_id', 'title', 'level']
)

print("\nNormalized DataFrame Shape:", df_courses.shape)
print(df_courses.head(10))

df_courses.to_csv('clean_course_catalog.csv', index=False)

print("\nSuccessfully created 'clean_course_catalog.csv'")
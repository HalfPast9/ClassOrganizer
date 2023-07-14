import json

year = '2023'
term = 'fall'
course_lst = ['SYSC-2006', 'SYSC-2310', 'MATH-1005', 'ELEC-2501', 'CCDP-2100']

course_data = []
for course in course_lst:
    location = f"course_data/{year}/{term}/{course}.json"
    with open(location, "r") as f:
        data = json.load(f)
        course_data.append(data)




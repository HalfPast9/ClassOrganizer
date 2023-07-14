import Courses as c
import json
from itertools import combinations


def data_collector(term, year, course_lst):
    """full_data = []
    courses = ['SYSC-2006', 'SYSC-2310', 'MATH-1005', "ELEC-2501", "CCDP-2100"]
    for course in courses:
        website_url = f'https://api.brethan.net/term/fall/2023/courseCode/{course}'
        response = requests.get(website_url)
        full_data.append(response.json())
    return full_data"""

    """course_str = ""
    with open(f"{file_name}", "r") as f:
        course_str += f.read()
        
    exec(f"course_data = {course_str}", locals())
    return locals()["course_data"]"""

    course_data = []
    for course in course_lst:
        location = f"course_data/{year}/{term}/{course}.json"
        with open(location, "r") as f:
            data = json.load(f)
            course_data.append(data)

    return course_data


def course_parser(data, course_lst):
    course = {
        'courseCode': None,
        'section': [],
        "time_slot": [],
        'course_type': [],
        'meeting_days': [],
        "letter_sets": [],
    }

    classes = []
    for i in range(len(course_lst)):
        sData = data[i]['data']

        for info in sData:
        
            course = c.Period()

            course.course_code = info['courseCode']
            course.section = info['section']
            course.time_slot = info['meetingInfo']['time']
            course.course_type = info['courseType']

            if len(info['meetingInfo']['days']) > 3:
                course.meeting_days = (info['meetingInfo']['days']).split(" ")
            else:
                course.meeting_days = [info['meetingInfo']['days']]
            
            if info['alsoRegister'] == None or info['alsoRegister'] == "Null":
                course.also_register = None
            else:
                course.also_register = info['alsoRegister']['sections']
            course.crn = info['crn']

            course.start_and_end()

            classes.append(course)
            if course.time_slot == None or course.time_slot == "Null":
                classes.pop()

    return(classes)

        
def time_conflict(course1,course2):

    check = False
    for i in course1.meeting_days:
        for j in course2.meeting_days:
            if i == j:
                check = True
                break

    if check:
        if course1.start_time <= course2.start_time <= course1.end_time:
            return True
        elif course1.start_time <= course2.end_time <= course1.end_time:
            return True
    
        elif course2.start_time <= course1.start_time <= course2.end_time:
            return True
        elif course2.start_time <= course1.end_time <= course2.end_time:
            return True
        

        elif course1.start_time == course2.start_time:
            return True
        elif course2.start_time == course1.start_time:
            return True
        elif course1.end_time == course2.end_time:
            return True
        
        else:
            return False
    
    else:
        return False

def schedule_length(course_lst):
    r = 0
    null_course = []
    for course in course_lst:
        if course.also_register:
            if course.course_code not in null_course:
                null_course.append(course.course_code)
                r += 2
        else:
            if course.course_code not in null_course:
                null_course.append(course.course_code)
                r += 1

    return r

def combination(arr, r):
  
    # return list of all subsets of length r
    # to deal with duplicate subsets use 
    # set(list(combinations(arr, r)))
    return list(combinations(arr, r))

def course_isolation(course_lst):
    courses = []
    tut = []
    for course in course_lst:
        if course.course_type != "Laboratory" and course.course_type != "Tutorial":
            courses.append(course)
        else:
            tut.append(course)
    
    return  courses, tut

def lecture_conflict(sched_lst):
    new_sched_lst = []
    for schedule in sched_lst:
        check = False
        for i in range(len(schedule)):
            for j in range(i + 1, len(schedule)):
                if schedule[i].course_code == schedule[j].course_code:
                    check = True
                    break
                if time_conflict((schedule[i]), (schedule[j])):
                    check = True
                    break  # Exit the inner loop if a duplicate is found

            if check:
                break  # Exit the outer loop if a duplicate is found

        if not check:
            new_sched_lst.append(schedule)

    sched_lst = new_sched_lst
                    
    return sched_lst

def valid_tut(course_lst, tut_lst):
    comb_lst = []

    for tutorial in tut_lst:
        check = 0
        tut_group = False
        
        for course in course_lst:
            if tutorial.course_code == course.course_code:
                    if tutorial.section in course.also_register:
                        tut_group = True
                        
            if time_conflict(tutorial, course) == False:
                check +=1
        

        if check == len(course_lst):
            if tut_group == True:
                comb_lst.append(tutorial)

    for course in course_lst:
        comb_lst.append(course)
    

    return comb_lst









        
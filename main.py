import accessories
from itertools import combinations

def main():
    day = []
    for i in range(30):
        day.append(None)
    
    year = '2023'
    term = 'fall'
    rqrd_courses = ['SYSC-2006', 'SYSC-2310', 'MATH-1005', "CCDP-2100", "ELEC-2501"]

    course_json = accessories.data_collector(term, year, rqrd_courses)
    course_lst = accessories.course_parser(course_json, rqrd_courses)

    lect_lst, tut_lst = accessories.course_isolation(course_lst)
    lect_sched = [list(comb) for comb in (accessories.combination(lect_lst,len(rqrd_courses)))]
    filt_lec = accessories.lecture_conflict(lect_sched)
    
    comb_lst = []
    for schedule in filt_lec:
        comb_lst.append(accessories.valid_tut(schedule, tut_lst))


    unfilt_scheds = []
    s_length = accessories.schedule_length(course_lst)
    for schedule in comb_lst:
        x = [list(comb) for comb in (accessories.combination(schedule, s_length))]
        for i in x:
            unfilt_scheds.append(i)
        print(f"{(comb_lst.index(schedule)+ 1)} of {len(comb_lst)}")
    
    """for i in unfilt_scheds:
        print("")
        print("[")
        for j in i:
            print(j.course_code, j.section, "    ", j.start_time, j.end_time, j.meeting_days)
        print("]")
    print(len(unfilt_scheds))"""

    scheds = []
    for schedule in unfilt_scheds:
        lect = []
        tut = []

        tut_check = []
        tut_check = set(tut_check)
        for course in schedule:

            if course.course_type != "Laboratory" and course.course_type != "Tutorial":
                lect.append(course)
            else:
                tut.append(course)


        for course in lect:
            for tutorial in tut:
                if course.also_register == None:
                    tut_check.add(course.course_code)
                else:
                    if course.course_code == tutorial.course_code:
                        tut_check.add(course.course_code)
        
        if len(lect) == len(rqrd_courses):
            if len(tut_check) == len(rqrd_courses):
                scheds.append(schedule)


    final_scheds = []
    for schedule in scheds:
        check = 0
        for i in range(len(schedule)):
            for j in range(i + 1, len(schedule)):
                if accessories.time_conflict(schedule[i], schedule[j]):
                    check += 1
        if check == 0:
            final_scheds.append(schedule)


    for i in range(len(final_scheds)):
         with open(f"schedules/schedule{i}.txt", "w") as f:
                for j in final_scheds[i]:
                    f.write(f"{j.course_code} {j.section} {j.start_time} {j.end_time} {j.meeting_days}\n")
                f.close()
    

    # go through the files and sort by best schdule based on factors like number of days off, consecuteive classes, etc.


        




import accessories
from itertools import combinations

def main():
    
    year = '2024'
    term = 'winter'
    rqrd_courses = [ "SYSC-2510", "SYSC-2100","SYSC-2004","MATH-2004","SYSC-2320"]
    print("Collecting Data...")
    course_json = accessories.data_collector(term, year, rqrd_courses)
    course_lst = accessories.course_parser(course_json, rqrd_courses)
    print("Data Collected")
    lect_lst, tut_lst = accessories.course_isolation(course_lst)
    lect_sched = [list(comb) for comb in (accessories.combination(lect_lst,len(rqrd_courses)))]
    filt_lec = accessories.lecture_conflict(lect_sched)
    print("Lecture Schedules Generated")
    comb_lst = []
    for schedule in filt_lec:
        comb_lst.append(accessories.valid_tut(schedule, tut_lst))
    print("Tutorial Schedules Generated")

    unfilt_scheds = []
    s_length = accessories.schedule_length(course_lst)
    for schedule in comb_lst:
        x = [list(comb) for comb in (accessories.combination(schedule, s_length))]
        for i in x:
            unfilt_scheds.append(i)
        print(f"{(comb_lst.index(schedule)+ 1)} of {len(comb_lst)}")
    
    print("Schedules Generated")
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

    print("Schedules Filtered")

    final_scheds = []
    for schedule in scheds:
        check = 0
        for i in range(len(schedule)):
            for j in range(i + 1, len(schedule)):
                if accessories.time_conflict(schedule[i], schedule[j]):
                    check += 1
        if check == 0:
            final_scheds.append(schedule)

    print("Schedules Filtered")
    print("writing to files")
    for i in range(len(final_scheds)):
         with open(f"schedules/schedule{i}.txt", "w") as f:
                for j in final_scheds[i]:
                    f.write(f"{j.course_code} {j.section} {j.start_time} {j.end_time} {j.meeting_days}\n")
                f.close()
    

    # go through the files and sort by best schdule based on factors like number of days off, consecuteive classes, etc.


        

main()


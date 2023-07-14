class Course:
    def __init__(self):
        pass


class Period:
    def __init__(self):
        self.course_code = ''
        self.section = ''
        self.time_slot = ''
        self.course_type = ''
        self.meeting_days = ''
        self.also_register = ''
        self.crn = ''
        pass

    def start_and_end(self):
        time_slot = (self.time_slot).split(" - ")
        start_lst = (time_slot[0]).split(":")
        end_lst = (time_slot[1]).split(":")
        self.start_time = ""
        self.end_time = ""
        for i in range(2):
            self.start_time += start_lst[i]
            self.end_time += end_lst[i]
        
        int(self.start_time)
        int(self.end_time)
    



        
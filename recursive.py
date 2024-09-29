class Person:
    def __init__(self, full_names, age, work_place, level_of_education, university_you_went_to):
        self.your_names = full_names
        self.your_age = age
        self.your_work_place = work_place
        self.your_level_of_education = level_of_education
        self.your_university = university_you_went_to
    def printname(self):
        print(self.your_names, self.your_age, self.your_work_place, self.your_level_of_education, self.your_university)

p = Person("My name is musinguzi Marcellinas",
            "aged 23",
            "working as a software developer in Silicon Valley",
            "and i persued a Bachelors of Science in Computer Science",
             "Uganda Christian University UCU")
p.printname()
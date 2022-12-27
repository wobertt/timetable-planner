from time_functions import LectureSlot

# a list of lecture slots that make up a complete timetable
Lectures = list[LectureSlot]

# a list of lecture slots for one course that must be taken together
LecturePackage = list[LectureSlot]

# maps course names to lecture slots
CourseOptions = dict[str, list[LecturePackage]]

# a list of lecture packages that contains every course once
CourseSelection = list[LecturePackage]

# a tuple of a penalty value and a complete (unpackaged) course selection
RatedCourseSelection = tuple[int, Lectures]

DAYS_OF_THE_WEEK = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday")

import pickle
from datatype_constants import CourseOptions, LecturePackage
from time_functions import LectureSlot, convert_to_24h


def process_input(raw_time: str, course_name: str) -> LectureSlot:
    """Return a LectureSlot object using the given course_name and raw_time.
    e.g., process_input('Tuesday 10:00AM - 12:00PM', 'CSCA08')

    """
    date, begin, _, end = raw_time.strip().split()
    return LectureSlot(
        course_name,
        date,
        convert_to_24h(begin),
        convert_to_24h(end)
    )


def read_line(prompt="") -> tuple[str, bool]:
    """Read and return a line of user input as a string.
    A flag of True is returned iff the user input was empty.

    """
    raw_input = input(prompt)
    return raw_input, raw_input == ""


def get_info(lectures: LecturePackage) -> frozenset[str]:
    """Get the info of each lecture in lectures."""
    return frozenset(
        f"{lecture.course_name}{lecture.day_num}{lecture.start_hour}{lecture.end_hour}" for lecture in lectures)


def read_lecture_timeslots(courses: CourseOptions, course_name: str, sections: int) -> None:
    """Read and add the lecture timeslots for course_name into courses.
    Lecture slots that go together are packaged in a list with size sections,
    and course_name is mapped to a list containing all such packages.

    """
    already_processed = set()  # catch duplicates

    grouping = []
    raw_input, is_empty = read_line("Enter timeslots (input empty line when done): ")
    while not is_empty:
        grouping.append(process_input(raw_input, course_name))
        if len(grouping) >= sections:
            lecture_info = get_info(grouping)
            if lecture_info not in already_processed:
                courses[course_name].append(grouping)
                already_processed.add(lecture_info)
            grouping = []
        raw_input, is_empty = read_line()


def process_all_input() -> CourseOptions:
    """Return a CourseOptions dictionary containing all course options read from user input.

    """
    courses = {}
    course_name, is_empty = read_line("Enter course name (input empty line when done): ")
    while not is_empty:
        courses[course_name] = []
        sections = int(input("Enter # of sessions per week: "))

        read_lecture_timeslots(courses, course_name, sections)

        course_name, is_empty = read_line("Enter course name (input empty line when done): ")

    return courses


def export_courses_to_file(file_name: str, courses: CourseOptions) -> None:
    """Write the contents of courses to the .pickle file file_name.
    """
    with open(file_name, 'wb') as f:
        pickle.dump(courses, f, pickle.HIGHEST_PROTOCOL)


def main() -> None:
    """Update a .pickle file to contain the inputted course selection options.

    """
    print("This code updates a .pickle file to contain course selection timetable options.")

    file_name = input("Enter a file name: ")
    if '.pickle' not in file_name:
        file_name += '.pickle'

    courses = process_all_input()
    export_courses_to_file(file_name, courses)
    print("Export complete!")


if __name__ == "__main__":
    main()

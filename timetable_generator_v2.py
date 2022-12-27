from datatype_constants import CourseOptions, RatedCourseSelection, CourseSelection, Lectures
from penalty_functions import get_total_penalty, MAX_CONSIDERATION
from itertools import product
import pickle


def unpackage_all_courses(selection: CourseSelection) -> Lectures:
    """Return a list containing all lecture slots in selection.

    """
    lectures = []
    for lecture_package in selection:
        for lecture_slot in lecture_package:
            lectures.append(lecture_slot)
    return lectures


def add_selection_results(all_selections: list[RatedCourseSelection], selection: CourseSelection) -> None:
    """Add the current course selection and its penalty value
    to all_selections, if the penalty does not exceed MAX_CONSIDERATION.

    """
    lectures = unpackage_all_courses(selection)
    penalty = get_total_penalty(lectures)
    if penalty <= MAX_CONSIDERATION:
        all_selections.append((
            get_total_penalty(lectures),
            lectures
        ))


def generate_all_selections(courses: CourseOptions) -> list[RatedCourseSelection]:
    all_selections = []
    processed_sets = set()
    for selection in product(*courses.values()):
        if str(selection) in processed_sets:
            continue
        add_selection_results(all_selections, selection)
        processed_sets.add(str(selection))
    return all_selections


def output_selection(processed_selection: RatedCourseSelection) -> None:
    """Output the total penalty and lecture times for each course in processed_selection.

    """
    print("Total penalty:", processed_selection[0])
    sorted_lectures = sorted(processed_selection[1], key=lambda lec: (lec.day_num, lec.end_hour))

    for lecture in sorted_lectures:
        lecture.output_info()


def output_all_selections(all_selections: list[RatedCourseSelection], max_output: int) -> None:
    """Output all course selections in all_selections in order of greatest-to-least penalty.
    At most max_output selections will be outputted.

    """
    all_selections.sort(key=lambda x: x[0], reverse=True)
    for selection in all_selections[-max_output:]:
        output_selection(selection)

    if len(all_selections) < max_output:
        print("Note: there aren't enough timetables that fit your requirements.")


def get_course_info(file_name: str) -> CourseOptions:
    """Return a CourseOptions dictionary containing the data in file_name.

    """
    with open(file_name, 'rb') as f:
        courses = pickle.load(f)
    return courses


def main(file_name: str) -> None:
    """Read from file_name and output the timetable results!
    """
    courses = get_course_info(file_name)

    print("Calculating results...")

    all_selections = generate_all_selections(courses)

    if not all_selections:
        print("Uh oh! There aren't any timetables that fit your requirements.")
        return

    num_selections = int(input("Results ready - How many options would you like to see? "))

    output_all_selections(all_selections, num_selections)


if __name__ == "__main__":
    pass
    # main('rachel_courses.pickle')

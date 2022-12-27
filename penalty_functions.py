from datatype_constants import LectureSlot, DAYS_OF_THE_WEEK

""" 

Penalty constants - feel free to change these!

OVERLAP_PENALTY            penalty for two lectures at same time
B2B_PENALTY                penalty for back-to-back lectures
EARLY_TUTORIAL_PENALTY     penalty for a tutorial early in the week (applied per day)
ONE_LECTURE_PENALTY        penalty for having a day_of_week with only one lecture
EARLIEST_HOUR, LATEST_HOUR earliest/latest lecture hours, in 24h time, that will not be penalized
EARLY_PENALTY              penalty for a lecture that starts earlier than EARLIEST_HOUR (applied per hour)
LATE_PENALTY               penalty for a lecture that ends later than LATEST_HOUR (applied per hour)
FRIDAY_PENALTY             penalty for a lecture on Friday

MAX_CONSIDERATION          (do not delete) maximum total penalty value for a selection to be considered
"""


MAX_CONSIDERATION = 5000
OVERLAP_PENALTY = 5000
B2B_PENALTY = 100
EARLY_TUTORIAL_PENALTY = 5
ONE_LECTURE_PENALTY = 1
EARLY_PENALTY, EARLIEST_HOUR = 2, 11
LATE_PENALTY, LATEST_HOUR = 10, 18
FRIDAY_PENALTY = 0

# This is the only function that communicates with timetable_generator_v2.py. It cannot be deleted.
# It can be freely modified as long as it is of the form list[LectureSlot] -> int
# All other functions can be deleted or modified as long as get_total_penalty runs correctly.
def get_total_penalty(lectures: list[LectureSlot]) -> int:
    """Return the total penalty value of lectures, calculated as the sum of all penalty types.

    Precondition: lectures contains all courses needed for a complete timetable.
    """
    return (
        get_overlap_penalty(lectures)
        + get_b2b_penalty(lectures)
        + get_early_late_penalty(lectures)
        + get_early_tutorial_penalty(lectures)
        + get_one_lecture_penalty(lectures)
        + get_friday_penalty(lectures)
    )


def get_all_lecture_pairs(lectures: list[LectureSlot]) -> list[tuple[LectureSlot, LectureSlot]]:
    """Return a list containing all possible pairs of lecture slots.
    """
    pairs = []
    for pos, lecture1 in enumerate(lectures):
        for lecture2 in lectures[pos + 1:]:
            pairs.append((lecture1, lecture2))
    return pairs


def get_lectures_on_day(lectures: list[LectureSlot], day: str) -> list[LectureSlot]:
    """Return a list containing all lectures on a given day.

    day must be 'Monday', 'Tuesday', 'Wednesday', 'Thursday', or 'Friday'.
    """
    return [lecture for lecture in lectures
            if lecture.day_of_week == day]


def is_overlapping(lecture1: LectureSlot, lecture2: LectureSlot) -> bool:
    """Returns True iff lecture1 and lecture2 overlap.
    Note: if one lecture ends when another lecture starts,
    they are considered to be back to back but NOT overlapping.
    """
    return (lecture1.day_num == lecture2.day_num
            and lecture1.start_hour < lecture2.end_hour
            and lecture2.start_hour < lecture1.end_hour)


def get_overlap_penalty(lectures: list[LectureSlot]) -> int:
    """Return a penalty value for overlapping courses,
    calculated as OVERLAP_PENALTY multiplied by
    the number of pairs of overlapping lecture slots.
    """
    overlap_count = 0
    for lecture1, lecture2 in get_all_lecture_pairs(lectures):
        if is_overlapping(lecture1, lecture2):
            overlap_count += 1
    return overlap_count * OVERLAP_PENALTY


def is_b2b(lecture1: LectureSlot, lecture2: LectureSlot) -> bool:
    """Return True iff lecture1 and lecture2 are back to back.
    """
    return (lecture1.day_num == lecture2.day_num and
            (lecture1.start_hour == lecture2.end_hour or lecture2.start_hour == lecture1.end_hour))


def get_b2b_penalty(lectures: list[LectureSlot]) -> int:
    """Return a penalty value for back-to-back courses,
    calculated as B2B_PENALTY multiplied by
    the number of pairs of back-to-back lecture slots.
    """
    b2b_count = 0
    for lecture1, lecture2 in get_all_lecture_pairs(lectures):
        if is_b2b(lecture1, lecture2):
            b2b_count += 1
    return b2b_count * B2B_PENALTY


def distance_from_friday(lecture: LectureSlot) -> int:
    """Return the distance from Friday, in days, of lecture."""
    return 5 - lecture.day_num


def get_early_tutorial_penalty(lectures: list[LectureSlot]) -> int:
    """Return a penalty value for tutorials that occur early in the week.
    """
    tutorial_penalty = 0
    for lecture in lectures:
        if lecture.course_name.endswith('TUT'):
            tutorial_penalty += distance_from_friday(lecture)
    return tutorial_penalty


def early_amount(lecture: LectureSlot) -> int:
    """Return the number of hours earlier than EARLIEST_HOUR that lecture starts at.
    """
    return max(0, EARLIEST_HOUR - lecture.start_hour)


def late_amount(lecture: LectureSlot) -> int:
    """Return the number of hours later than LATEST_HOUR that lecture ends at.
    """
    return max(0, lecture.end_hour - LATEST_HOUR)


def get_early_late_penalty(lectures: list[LectureSlot]) -> int:
    """Return a penalty value for early or late courses.
    """
    time_penalty = 0
    for lecture in lectures:
        time_penalty += early_amount(lecture) * EARLY_PENALTY + late_amount(lecture) * LATE_PENALTY
    return time_penalty


def get_one_lecture_penalty(lectures: list[LectureSlot]) -> int:
    """Return a penalty value for days of the week that contain exactly one lecture.
    """
    day_penalty = 0
    for day in DAYS_OF_THE_WEEK:
        if len(get_lectures_on_day(lectures, day)) == 1:
            day_penalty += ONE_LECTURE_PENALTY
    return day_penalty


def get_friday_penalty(lectures: list[LectureSlot]) -> int:
    """Return FRIDAY_PENALTY if there is a lecture on Friday, and 0 otherwise.
    """
    if get_lectures_on_day(lectures, 'Friday'):
        return FRIDAY_PENALTY
    return 0


# Run the timetable generator
if __name__ == "__main__":
    import timetable_generator_v2
    timetable_generator_v2.main('cms_plus_copb51_cscb20.pickle')

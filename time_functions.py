def convert_to_12h(time_24h: int) -> str:
    """Return a 12h representation of time_24h.

    >>> convert_to_12h(16)
    '4:00PM'
    >>> convert_to_12h(12)
    '12:00PM'
    >>> convert_to_12h(5)
    '5:00AM'
    """
    if time_24h > 12:
        return f"{time_24h - 12}:00PM"
    if time_24h == 12:
        return f"{time_24h}:00PM"
    return f"{time_24h}:00AM"


def convert_to_24h(time_12h: str) -> int:
    """Return the 24h equivalent of time_12h (in hours, rounded down).

    >>> convert_to_24h('4:00PM')
    16
    >>> convert_to_24h('12:00PM')
    12
    >>> convert_to_24h('5:00AM')
    5
    """
    time_24h = int(time_12h.split(':')[0]) % 12
    if time_12h[-2:] == 'PM':
        return time_24h + 12
    return time_24h


class LectureSlot:
    """
    Stores the name and time info of some lecture slot.
    """
    def __init__(self, course_name: str, day: str, begin: int, end: int):
        self.course_name = course_name
        self.day_of_week = day
        self.day_num = LectureSlot.day_map[day]
        self.start_hour = begin
        self.end_hour = end

    day_map = {     # There shouldn't be any courses on weekends
        'Monday': 1,
        'Tuesday': 2,
        'Wednesday': 3,
        'Thursday': 4,
        'Friday': 5,
    }

    def output_info(self) -> None:
        """
        Print a LectureSlot in the form COURSECODE - DayOfWeek: XXAM-XXPM
        """
        print(f"{self.course_name} - {self.day_of_week}: "
              f"{convert_to_12h(self.start_hour)}-{convert_to_12h(self.end_hour)}")

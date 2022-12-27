# timetable-planner

### How do I generate my timetables?

1. Open `penalty_functions.py` and scroll to the bottom of the file.
2. Put the name of your `.pickle` file as a string argument to `timetable_generator_v2.main()`.
3. Run the code!


### How do I make a new `.pickle` file?

See `input_course_info.py` - Ask Robert for details.


### I don't like the timetable results. How can I improve them?

Read about the penalty constants at the top of `penalty_functions.py`.
Experiment with different values and see what you like!


### The current penalty options are not flexible enough for me. Can I make new constants?

Absolutely! Just remember that all constants and functions are helpers for `get_total_penalty()`,
so you will need to update `get_total_penalty()` to use your new code.

You may find the functions `get_all_lecture_pairs()` and `get_lectures_on_day()` helpful.


### What are the `LectureSlot` and `list[LectureSlot]` datatypes?

`LectureSlot` is a class that packages some useful information about lectures. See `time_functions.py` for details.

Suppose there is a variable `x` whose type is `LectureSlot`.
You can access the following attributes as if they were variables:

| Attribute       | Type |          Example values         |
|:---------------:|:----:|:-------------------------------:|
|  `x.course_name`  |  `str` |   `'CSCA08'`, `'A48TUT'`, `'MATA37'`  |
|  `x.day_of_week`  |  `str` | `'Monday'`, `'Wednesday'`, `'Friday'` |
|    `x.day_num`    |  `int` |             `1`, `3`, `5`             |
|   `x.start_hour`  |  `int` |       `9`, `12`, `20`      |
|    `x.end_hour`   |  `int` |      `11`, `15`, `22` |

`list[LectureSlot]` is a list of lecture slots. When a `list[LectureSlot]` is passed to `get_total_penalty()`, it will always be a complete timetable.

import os
from datetime import date, datetime
from dataclasses import dataclass
from collections import defaultdict
from typing import Dict, List, Tuple
from sheet_parser import MappedSlot
from core import constants
from core.utils.datetime_util import DatetimeUtil


@dataclass
class MappedCourse:
    course_code: str = ""
    course_name: str = ""
    main_teacher_code: str = ""
    required_flag: bool = None
    credit: int = None
    class_code: str = ""
    class_name: str = ""
    school_user_id: str = ""
    threshold_lateness_time: int = None
    threshold_absense_time: int = None
    threshold_absense_conut: int = None
    start_time: datetime = None
    end_time: datetime = None
    room: str = ""
    continue_flag: bool = None

    def get_csv_schema(self) -> str:
        properties = self.__annotations__.keys()

        return ",".join(list(properties))

    def to_csv_row(self) -> str:
        row = ""
        for v in self.__dict__.values():
            row += str(v) if v is not None else ""
            row += ","

        return row[:-1]


class CsvWriter:
    def handle(
        self,
        output_path: str,
        file_name: str,
        date_slot_map: Dict[date, Dict[int, Dict[str, MappedSlot]]],
    ) -> None:
        # organize parsed content into target csv schema
        course_slot_map = self.__init_course_slot_map()
        for scheduled_date, slots in date_slot_map.items():
            for slot, courses in slots.items():
                for course, mapped_slot in courses.items():
                    group_mapped_course_map = (
                        self.__convert_mapped_slot_to_mapped_course(
                            mapped_slot, course, slot, scheduled_date
                        )
                    )
                    for group, mapped_course in group_mapped_course_map.items():
                        course_slot_map[course][group].append(mapped_course)

        output_content = self.__format_csv_content(course_slot_map)

        # write content into target file
        path = os.path.join(output_path, file_name)
        self.__write_csv(path, output_content)
        print(f"Done outputting {path}")

    def __init_course_slot_map(self) -> Dict[str, Dict[str, List[MappedCourse]]]:
        return defaultdict(lambda: defaultdict(list))

    def __convert_mapped_slot_to_mapped_course(
        self, mapped_slot: MappedSlot, course_name: str, slot: int, scheduled_date: date
    ) -> Dict[str, MappedCourse]:
        group_mapped_course_map: Dict[str, MappedCourse] = dict()

        if len(mapped_slot.groups) == 0:
            start_time, end_time = self.__calculate_lecture_period(scheduled_date, slot)
            mapped_course = MappedCourse(
                course_name=course_name,
                class_name=course_name,
                start_time=start_time,
                end_time=end_time,
                room="/".join(mapped_slot.rooms),
            )

            group_mapped_course_map[course_name] = mapped_course

        elif len(mapped_slot.groups) == len(mapped_slot.rooms):
            for group, room in zip(mapped_slot.groups, mapped_slot.rooms):
                class_name = course_name + ": " + group
                start_time, end_time = self.__calculate_lecture_period(
                    scheduled_date, slot
                )
                mapped_course = MappedCourse(
                    course_name=course_name,
                    class_name=class_name,
                    start_time=start_time,
                    end_time=end_time,
                    room=room,
                )
                group_mapped_course_map[class_name] = mapped_course

        elif len(mapped_slot.rooms) % len(mapped_slot.groups) == 0:
            pass

        else:
            raise Exception(
                f"cannot properly arrange rooms to each group: {mapped_slot}"
            )

        return group_mapped_course_map

    def __calculate_lecture_period(
        self, scheduled_date: date, slot: int
    ) -> Tuple[datetime, datetime]:
        start_time = DatetimeUtil.conbine_date_and_time(
            date=scheduled_date,
            time=constants.SLOT_START_TIME_MAP[slot],
        )
        end_time = DatetimeUtil.calculate_next_n_minutes(
            start_time, constants.DEFAULT_LECTURE_PERIOD
        )

        return start_time, end_time

    def __format_csv_content(
        self, course_slot_map: Dict[str, Dict[str, List[MappedCourse]]]
    ) -> List[str]:
        content: List[str] = list()

        for group_mapped_course_list_map in course_slot_map.values():
            for mapped_course_list in group_mapped_course_list_map.values():
                for mapped_course in mapped_course_list:
                    content.append(mapped_course.to_csv_row())

        return content

    def __write_csv(self, path: str, body: List[str]):
        path += ".csv"
        header = MappedCourse().get_csv_schema()
        content = header + "\n" + "\n".join(body)

        with open(path, "w") as f:
            f.write(content)

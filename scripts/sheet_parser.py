import re
from typing import Dict, List, Tuple, Optional
from datetime import date
from dataclasses import dataclass, field
from collections import defaultdict
from core import constants
from core.utils.excel_parser_util import ExcelParserUtil
from core.utils.string_normalizer_util import StringNormalizerUtil
from core.utils.date_parser_util import DateParserUtil
from core.utils.date_util import DateUtil


@dataclass
class MappedSlot:
    groups: List[str] = field(default_factory=list)
    rooms: List[str] = field(default_factory=list)


class SheetParser:
    def handle(
        self, sheet_name: str, content: List[List]
    ) -> Dict[date, Dict[int, Dict[str, MappedSlot]]]:
        course_slot_map = self.__init_course_slot_map()
        time_slots, body = self.__parse_sheet_component(content)
        base_year, base_month, base_day = self.__parse_base_date(sheet_name, body)
        target_grade = self.__parse_target_grade(sheet_name)
        calendar_date = DateUtil.construct_date(base_year, base_month, base_day)

        for row_idx, row in enumerate(body):
            for col_idx, cell in enumerate(row[2:-1]):
                cell = StringNormalizerUtil.handle(str(cell)).strip()
                if cell == "":
                    continue

                slot, calendar_date = self.__parse_slot(
                    str(time_slots[col_idx]), calendar_date
                )
                if slot < 0:
                    continue

                subject_name, groups, rooms, should_skip = self.__parse_cell(cell)
                if should_skip:
                    continue

                if len(rooms) == 0:
                    # assign default room
                    rooms = [constants.DEFAULT_GRADE_ROOM_MAP[target_grade]]

                if subject_name is None:
                    # if only contains rooms info
                    registered_keys = course_slot_map[calendar_date][slot].keys()
                    if len(registered_keys) != 1:
                        raise Exception(f"ERROR: '{cell}' is not properly formatted.")
                    subject_name = list(registered_keys)[0]
                    course_slot_map[calendar_date][slot][subject_name].rooms = rooms
                else:
                    course_slot_map[calendar_date][slot][subject_name].groups = groups
                    course_slot_map[calendar_date][slot][subject_name].rooms = rooms

            # assume Saturday is the last week_date
            if self.__is_second_line_of_the_day(row_idx):
                calendar_date = DateUtil.calculate_next_n_day(calendar_date, 2)
            else:
                calendar_date = DateUtil.calculate_next_n_day(calendar_date, -5)

        return course_slot_map

    def __init_course_slot_map(
        self,
    ) -> Dict[date, Dict[int, Dict[str, MappedSlot]]]:
        return defaultdict(lambda: defaultdict(lambda: defaultdict(MappedSlot)))

    def __parse_sheet_component(
        self, sheet_content: List[List]
    ) -> Tuple[List, List[List]]:
        header, body = ExcelParserUtil.parse_sheet(sheet_content)
        time_slots = header[2:]

        return time_slots, body

    def __parse_base_date(
        self, sheet_name: str, sheet_body: List[List]
    ) -> Tuple[int, int, int]:
        base_year = DateParserUtil.parse_year(sheet_name)
        base_month = DateParserUtil.parse_month(
            StringNormalizerUtil.handle(str(sheet_body[0][0]))
        )
        base_day = DateParserUtil.parse_day(
            StringNormalizerUtil.handle((str(sheet_body[0][1])))
        )

        return base_year, base_month, base_day

    def __parse_target_grade(self, sheet_name: str) -> int:
        _, grade_str, _ = sheet_name.split("-")

        if re.match(constants.TRANSFERED_GRADE_REGEX, grade_str):
            # if target sheet is for transferred students
            grade_str = grade_str[:-1]

        return int(grade_str)

    def __parse_slot(self, slot_str: str, calendar_date: date) -> Tuple[int, date]:
        slot_str = StringNormalizerUtil.handle(slot_str)
        slot = DateParserUtil.parse_slot(slot_str)
        if slot < 0:
            calendar_date = DateUtil.calculate_next_n_day(calendar_date, 1)

        return slot, calendar_date

    def __parse_cell(self, cell: str) -> Tuple[Optional[str], List, List, bool]:
        subject_name, groups, rooms, should_skip = None, list(), list(), False
        exploded = cell.split(" ")
        if len(exploded) == 1:
            # if the cell consists of either [subject] or [rooms]
            v = exploded[0]
            if v in constants.SUBJECT_ABBREVIATION_MAP:
                subject_name = constants.SUBJECT_ABBREVIATION_MAP[v]
            elif re.match(constants.ROOM_INFO_REGEX, v):
                rooms = v[1:-1].split("/")
            else:
                should_skip = True

        elif len(exploded) == 2:
            # if the cell consists of either [subject, groups] or [subject, rooms]
            v1, v2 = exploded
            if v1 not in constants.SUBJECT_ABBREVIATION_MAP:
                should_skip = True
            else:
                subject_name = constants.SUBJECT_ABBREVIATION_MAP[v1]
                if re.match(constants.GROUP_INFO_REGEX, v2):
                    groups = list(v2)
                elif re.match(constants.ROOM_INFO_REGEX, v2):
                    rooms = v[1:-1].split("/")
                else:
                    raise Exception(f"ERROR: '{v2}' is not properly formatted.")

        elif len(exploded) == 3:
            # if the cell consists of [subject, groups, rooms]
            v1, v2, v3 = exploded
            if v1 not in constants.SUBJECT_ABBREVIATION_MAP:
                should_skip = True
            else:
                subject_name = constants.SUBJECT_ABBREVIATION_MAP[v1]

                if re.match(constants.GROUP_INFO_REGEX, v2):
                    groups = list(v2)
                else:
                    raise Exception(f"ERROR: '{v2}' is not properly formatted.")

                if re.match(constants.ROOM_INFO_REGEX, v3):
                    rooms = v3[1:-1].split("/")
                else:
                    raise Exception(f"ERROR: '{v3}' is not properly formatted.")

        return subject_name, groups, rooms, should_skip

    def __is_second_line_of_the_day(self, row_idx: int) -> bool:
        # assume each schedule consists of 2 rows
        return row_idx % 2 != 0

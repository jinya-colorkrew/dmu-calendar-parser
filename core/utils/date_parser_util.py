import re
from core import constants


class DateParserUtil:
    def parse_year(s: str) -> int:
        m = re.match(constants.YEAR_REGEX, s)
        if m is None:
            raise Exception(f"'{s}' doesn't match the regex patter for YEAR")

        return int(m.group())

    def parse_month(s: str) -> int:
        if s == "":
            return -1

        m = re.match(constants.MONTH_REGEX, s)
        if m is None:
            raise Exception(f"'{s}' doesn't match the regex pattern for MONTH")

        return int(m.group()[:-1])

    def parse_day(s: str) -> int:
        if s == "":
            return -1

        return int(s)

    def parse_slot(s: str) -> int:
        if s == "":
            return -1

        return int(s)

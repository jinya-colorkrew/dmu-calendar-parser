from datetime import timedelta
from datetime import date


class DateUtil:
    def construct_date(year, month, day) -> date:
        return date(year, month, day)

    def calculate_next_n_day(org_date: date, n: int) -> date:
        return org_date + timedelta(days=n)

import pytz
from datetime import datetime, date, timedelta, time
from core import constants


class DatetimeUtil:
    def calculate_next_n_minutes(org_dt: datetime, n: int) -> datetime:
        return org_dt + timedelta(minutes=n)

    def conbine_date_and_time(
        date: date, time: time, tz: str = constants.DEFAULT_TIMEZONE
    ):
        combined_dt = datetime.combine(date, time)
        dt_with_timezone = pytz.timezone(tz).localize(combined_dt)

        return dt_with_timezone

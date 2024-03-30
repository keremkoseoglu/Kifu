""" Date time stuff """
import datetime
import re
import requests
from ics import Calendar
import config


_FIRST_MONTH = 1
_MAX_MONTH = 12
_MONTHS = [
    "January",
    "February",
    "March",
    "April",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]
_TURKISH_DATE_LEN = 10
_TURKISH_DATE_REGEX = "[0-3][0-9].[0-1][0-9].[1-2][0-9][0-9][0-9]"
_BANK_HOLIDAY_CALENDAR = None


def equals(date1: datetime.datetime, date2: datetime.datetime):
    """Do both dates equal"""
    if (
        date1.year == date2.year
        and date1.month == date2.month
        and date1.day == date2.day
    ):
        return True
    return False


def get_first_day_of_month(date: datetime.datetime):
    """First day of month"""
    year = date.year
    month = date.month
    return datetime.datetime(year=year, month=month, day=1)


def get_first_day_of_next_month(date: datetime.datetime):
    """First day of next month"""
    year = date.year
    month = date.month
    if month == _MAX_MONTH:
        year += 1
        month = 1
    else:
        month += 1
    return datetime.datetime(year=year, month=month, day=1)


def get_formatted_date(date: datetime.datetime) -> str:
    """Formatted date"""
    return date.isoformat()[:10]


def get_official_turkish_date(date: datetime.datetime) -> str:
    """06.12.2022 format"""
    year = date.year
    month = get_two_digit_month(date.month)
    day = get_two_digit_month(date.day)
    return f"{ str(day) }.{ str(month) }.{str(year)}"


def get_last_day_of_prev_month(date: datetime.datetime) -> datetime:
    """Last day of previous month"""
    previous_month = get_previous_month(date)
    year = previous_month.year
    month = previous_month.month
    day = _get_last_day_of_month(month, year)
    return datetime.datetime(year=year, month=month, day=day)


def get_last_day_of_month(date: datetime.datetime) -> datetime:
    """Last day of given month"""
    year = date.year
    month = date.month
    day = _get_last_day_of_month(month, year)
    return datetime.datetime(year=year, month=month, day=day)


def get_mid_day_of_month(date: datetime.datetime):
    """Middle day of month"""
    year = date.year
    month = date.month
    return datetime.datetime(year=year, month=month, day=15)


def get_mid_day_of_next_month(date: datetime.datetime):
    """Middle day of next month"""
    date2 = get_next_month(date)
    year = date2.year
    month = date2.month
    return datetime.datetime(year=year, month=month, day=15)


def get_mid_day_of_next_year(date: datetime.datetime):
    """Middle day of next year"""
    return get_next_year(get_mid_day_of_year(date))


def get_mid_day_of_year(date: datetime.datetime):
    """Middle day of year"""
    year = date.year
    return datetime.datetime(year=year, month=6, day=15)


def get_month_name(month: int) -> str:
    """Name of given month"""
    return _MONTHS[month]


def get_months_between_dates(low: datetime.datetime, high: datetime.datetime) -> int:
    """Calculates and returns months between dates"""
    return (high.year - low.year) * 12 + (high.month - low.month)


def get_next_day(date: datetime.datetime, next_count=1):
    """Tomorrow, tomorrow, I love you, tomorrow"""
    return date + datetime.timedelta(days=next_count)


def get_next_month(date: datetime, next_count=1):
    """Next month"""
    next_year = date.year
    next_month = date.month + next_count
    while next_month > _MAX_MONTH:
        next_month -= _MAX_MONTH
        next_year += 1

    day = _shift_day_to_month(date.day, next_month, next_year)
    return datetime.datetime(year=next_year, month=next_month, day=day)


def get_next_week(date: datetime, next_count=1):
    """Next week"""
    return date + datetime.timedelta(weeks=next_count)


def get_nearest_workday(date: datetime, backwards=False):
    """Nearest workday"""
    output = date

    try:
        while output.weekday() == 5 or output.weekday() == 6 or is_bank_holiday(output):
            if backwards:
                output = get_next_day(output, next_count=-1)
            else:
                output = get_next_day(output, next_count=1)
    except Exception as error:
        print(error)

    return output


def get_next_year(date: datetime, next_count=1):
    """Next year"""
    return datetime.datetime(date.year + next_count, date.month, date.day)


def get_previous_month(date: datetime) -> datetime:
    """Previous month"""
    year = date.year
    month = date.month

    month -= 1
    if month == 0:
        month = 12
        year -= 1

    day = _shift_day_to_month(date.day, month, year)
    return datetime.datetime(year=year, month=month, day=day)


def get_turkish_date_at_start(line: str) -> datetime.datetime:
    """Turkish formatted"""
    split_line = line.split(";")

    if len(split_line) < 2:
        return None

    date_part = split_line[0]
    date_candidate = date_part.split(".")
    if len(date_candidate) < 3:
        return None

    day_part = str(date_candidate[0])
    while len(day_part) < 2:
        day_part = "0" + day_part

    month_part = str(date_candidate[1])
    while len(month_part) < 2:
        month_part = "0" + month_part

    year_part = str(date_candidate[2])

    start_of_line = day_part + "." + month_part + "." + year_part

    if not is_turkish_date(start_of_line):
        return None
    return parse_turkish_date(start_of_line)


def get_two_digit_month(month: int) -> str:
    """Two digit month"""
    output = str(month)
    while len(output) < 2:
        output = "0" + output
    return output


def is_bank_holiday(date: datetime) -> bool:
    """Is bank holiday"""
    global _BANK_HOLIDAY_CALENDAR

    if _BANK_HOLIDAY_CALENDAR is None:
        _BANK_HOLIDAY_CALENDAR = Calendar(
            requests.get(config.CONSTANTS["BANK_HOLIDAY_URL"], timeout=10).text
        )

    for holiday_event in _BANK_HOLIDAY_CALENDAR.events:
        holiday_begin = datetime.datetime(
            year=holiday_event.begin.datetime.year,
            month=holiday_event.begin.datetime.month,
            day=holiday_event.begin.datetime.day,
        )

        holiday_end = datetime.datetime(
            year=holiday_event.end.datetime.year,
            month=holiday_event.end.datetime.month,
            day=holiday_event.end.datetime.day,
        )

        if date >= holiday_begin and date < holiday_end:  # pylint: disable=R1716
            return True

    return False


def is_today(date: datetime) -> bool:
    """Is date today"""
    return equals(date, datetime.datetime.now())


def is_turkish_date(date: str) -> bool:
    """Is the given date a Turkish date"""
    return re.compile(_TURKISH_DATE_REGEX).match(date) is not None


def is_working_day(date: datetime) -> bool:
    """Is the given date a working day"""
    weekday = date.weekday()
    if weekday in (5, 6):
        return False
    if is_bank_holiday(date):
        return False
    return True


def parse_json_date(json_date: str) -> datetime:
    """Parses a JSON date"""
    try:
        return datetime.datetime.strptime(json_date, "%Y-%m-%dT%H:%M:%S.%f")
    except Exception:
        pass

    try:
        return datetime.datetime.strptime(json_date, "%Y-%m-%dT%H:%M:%S.%fZ")
    except Exception:
        pass

    try:
        return datetime.datetime.strptime(json_date, "%Y-%m-%d %H:%M:%S.%f")
    except Exception:
        pass

    try:
        return datetime.datetime.strptime(json_date, "%Y-%m-%dT%H:%M:%S")
    except Exception:
        pass

    try:
        return datetime.datetime.strptime(json_date, "%Y-%m-%d %H:%M:%S")
    except Exception:
        pass

    return datetime.datetime.strptime(json_date, "%Y-%m-%d")


def parse_sap_date(date: str) -> datetime.datetime:
    """Parse date in SAP format"""
    year = int(date[0] + date[1] + date[2] + date[3])
    month = int(date[4] + date[5])
    day = int(date[6] + date[7])
    return datetime.datetime(year=year, month=month, day=day)


def parse_turkish_date(date: str) -> datetime.datetime:
    """Parse date in Turkish format"""
    try:
        str_date = (
            get_official_turkish_date(date)
            if isinstance(date, datetime.datetime)
            else date
        )
        split_date = str_date.split(".")
        year = int(split_date[2])
        month = int(split_date[1])
        day = int(split_date[0])
        return datetime.datetime(year=year, month=month, day=day)
    except Exception as date_error:
        raise date_error


def _month_has_30_days(month: int) -> bool:
    return month in (4, 6, 9, 11)


def _get_last_day_of_month(month: int, year: int) -> int:
    if month == 2 and year % 4 == 0:
        return 29
    if month == 2:
        return 28
    if _month_has_30_days(month):
        return 30
    return 31


def _shift_day_to_month(day: int, month: int, year: int) -> int:
    last_day_of_month = _get_last_day_of_month(month, year)
    if day > last_day_of_month:
        return last_day_of_month
    return day

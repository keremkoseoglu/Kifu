import datetime, re, requests
from ics import Calendar
from config.constants import *

_FIRST_MONTH = 1
_MAX_MONTH = 12
_MONTHS = ["January", "February", "March", "April", "June", "July", "August", "September", "October", "November", "December"]
_TURKISH_DATE_LEN = 10
_TURKISH_DATE_REGEX = "[0-3][0-9].[0-1][0-9].[1-2][0-9][0-9][0-9]"
_BANK_HOLIDAY_CALENDAR = None


def equals(date1: datetime.datetime, date2: datetime.datetime):
    if date1.year == date2.year and date1.month == date2.month and date1.day == date2.day:
        return True
    else:
        return False


def get_first_day_of_month(date: datetime.datetime):
    year = date.year
    month = date.month
    return datetime.datetime(year=year, month=month, day=1)


def get_first_day_of_next_month(date:datetime.datetime):
    year = date.year
    month = date.month
    if month == _MAX_MONTH:
        year += 1
        month = 1
    else:
        month += 1
    return datetime.datetime(year=year, month=month, day=1)


def get_formatted_date(date: datetime.datetime) -> str:
    return date.isoformat()[:10]


def get_last_day_of_prev_month(date: datetime.datetime) -> datetime:
    previous_month = get_previous_month(date)
    year = previous_month.year
    month = previous_month.month

    if month == 2:
        if year % 4 == 0:
            day = 29
        else:
            day = 28
    elif month == 4 or month == 6 or month == 9 or month == 11:
        day = 30
    else:
        day = 31

    return datetime.datetime(year=year, month=month, day=day)


def get_last_day_of_month(date: datetime.datetime) -> datetime:
    year = date.year
    month = date.month
    day = 31
    if month == 2 and year % 4 == 0:
        day = 28
    elif month == 4 or month == 6 or month == 9 or month == 11:
        day = 30
    return datetime.datetime(year=year, month=month, day=day)


def get_mid_day_of_month(date: datetime.datetime):
    year = date.year
    month = date.month
    return datetime.datetime(year=year, month=month, day=15)


def get_mid_day_of_next_month(date: datetime.datetime):
    date2 = get_next_month(date)
    year = date2.year
    month = date2.month
    return datetime.datetime(year=year, month=month, day=15)


def get_mid_day_of_next_year(date:datetime.datetime):
    return get_next_year(get_mid_day_of_year(date))


def get_mid_day_of_year(date: datetime.datetime):
    year = date.year
    return datetime.datetime(year=year, month=6, day=15)


def get_month_name(month: int) -> str:
    return _MONTHS[month]


def get_next_day(date:datetime.datetime, next_count=1):
    return date + datetime.timedelta(days=next_count)


def get_next_month(date:datetime, next_count=1):
    next_year = date.year
    next_month = date.month + next_count
    while next_month > _MAX_MONTH:
        next_month -= _MAX_MONTH
        next_year += 1
    day = date.day
    if next_month == 2 and day > 28:
        day = 28
    elif (next_month == 4 or next_month == 6 or next_month == 9 or next_month == 11) and day > 30:
        day = 30
    return datetime.datetime(year=next_year, month=next_month, day=day)


def get_next_week(date:datetime, next_count=1):
    return date + datetime.timedelta(weeks=next_count)


def get_nearest_workday(date: datetime, backwards=False):

    output = date

    while output.weekday() == 5 or output.weekday() == 6 or is_bank_holiday(output):
        if backwards:
            output = get_next_day(output, next_count=-1)
        else:
            output = get_next_day(output, next_count=1)

    return output


def get_next_year(date: datetime, next_count=1):
    return datetime.datetime(date.year+next_count, date.month, date.day)


def get_previous_month(date:datetime) -> datetime:
    year = date.year
    month = date.month
    day = date.day

    month -= 1
    if month == 0:
        month = 12
        year -= 1

    if month == 2:
        if day > 29:
            day = 29
        if day == 29:
            if year % 4 != 0:
                day = 28
    elif month == 4 or month == 6 or 9 or month == 11:
        if day > 30:
            day = 30

    return datetime.datetime(year=year, month=month, day=day)


def get_turkish_date_at_start(line: str) -> datetime.datetime:
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
    output = str(month)
    while len(output) < 2:
        output = "0" + output
    return output


def is_bank_holiday(date: datetime) -> bool:
    global _BANK_HOLIDAY_CALENDAR

    if _BANK_HOLIDAY_CALENDAR is None:
        _BANK_HOLIDAY_CALENDAR = Calendar(requests.get(BANK_HOLIDAY_URL).text)

    for holiday_event in _BANK_HOLIDAY_CALENDAR.events:
        holiday_begin = datetime.datetime(year=holiday_event.begin.datetime.year,
                                          month=holiday_event.begin.datetime.month,
                                          day=holiday_event.begin.datetime.day)

        holiday_end = datetime.datetime(year=holiday_event.end.datetime.year,
                                        month=holiday_event.end.datetime.month,
                                        day=holiday_event.end.datetime.day)

        if date >= holiday_begin and date < holiday_end:
            return True

    return False


def is_today(date: datetime) -> bool:
    return equals(date, datetime.datetime.now())


def is_turkish_date(date: str) -> bool:
    if re.compile(_TURKISH_DATE_REGEX).match(date) is not None:
        return True
    else:
        return False


def is_working_day(date: datetime) -> bool:
    weekday = date.weekday()
    if weekday == 5 or weekday == 6:
        return False
    elif is_bank_holiday(date):
        return False
    else:
        return True

def parse_json_date(json_date: str) -> datetime:
    try:
        return datetime.datetime.strptime(json_date, '%Y-%m-%dT%H:%M:%S.%f')
    except:
        pass

    try:
        return datetime.datetime.strptime(json_date, '%Y-%m-%dT%H:%M:%S.%fZ')
    except:
        pass

    try:
        return datetime.datetime.strptime(json_date, '%Y-%m-%d %H:%M:%S.%f')
    except:
        pass

    try:
        return datetime.datetime.strptime(json_date, '%Y-%m-%dT%H:%M:%S')
    except:
        pass

    try:
        return datetime.datetime.strptime(json_date, '%Y-%m-%d %H:%M:%S')
    except:
        pass

    return datetime.datetime.strptime(json_date, '%Y-%m-%d')


def parse_sap_date(date: str) -> datetime.datetime:
    year = int(date[0] + date[1] + date[2] + date[3])
    month = int(date[4] + date[5])
    day = int(date[6] + date[7])
    return datetime.datetime(year=year, month=month, day=day)


def parse_turkish_date(date: str) -> datetime.datetime:
    split_date = date.split(".")
    year = int(split_date[2])
    month = int(split_date[1])
    day = int(split_date[0])
    return datetime.datetime(year=year, month=month, day=day)



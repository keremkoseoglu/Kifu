""" Workdays without activity API """
from datetime import timedelta, datetime
from model.activity import Activity
from util.date_time import is_working_day, get_last_day_of_month


def _short_date(date: datetime) -> str:
    return str(date)[:10]


class WorkdaysWoActivityAPI():
    """ Workdays without activity API """
    def __init__(self):
        self._activities = []
        self._dates = []
        self._out = {}

    @property
    def result(self) -> dict:
        """ Returns net worth """
        if "Days" not in self._out:
            self._out = {"Days": []}

            self._read_activities()
            self._build_date_range()
            self._build_output()

        return self._out

    def _read_activities(self):
        self._activities = []
        for activity_dict in Activity.get_activities()["activities"]:
            self._activities.append(Activity(activity_dict))
        sorted(self._activities, key=lambda activity: activity.date)

    def _build_date_range(self):
        self._dates = []
        first_date = self._activities[0].date
        last_date = self._activities[len(self._activities) - 1].date
        last_date = get_last_day_of_month(last_date)
        date_cursor = first_date
        while date_cursor <= last_date:
            self._dates.append(date_cursor)
            date_cursor += timedelta(days=1)

    def _has_activity_on_date(self, date: datetime) -> bool:
        for activity in self._activities:
            if _short_date(activity.date) == _short_date(date):
                return True
        return False

    def _build_output(self):
        for date in self._dates:
            workday = is_working_day(date)
            has_activity = self._has_activity_on_date(date)
            workday_alert = False
            workday_no_alert = False
            icon = ""

            if workday:
                holiday = False
                day_status = "Workday"
                if has_activity:
                    act_status = "Has activity"
                    color = "green"
                    workday_no_alert = True
                    icon = "🟢"
                else:
                    act_status = "No activity"
                    workday_alert = True
                    color = "red"
                    icon = "🔴"
            else:
                holiday = True
                day_status = "Holiday"
                act_status = "-"
                color = "gray"
                icon = "⚪️"

            day_dict = {"date": _short_date(date),
                        "workday": workday,
                        "holiday": holiday,
                        "day": date.strftime("%A"),
                        "has_activity": has_activity,
                        "workday_alert": workday_alert,
                        "workday_no_alert": workday_no_alert,
                        "icon": icon,
                        "act_status": act_status,
                        "day_status": day_status,
                        "color": color}

            self._out["Days"].append(day_dict)
        
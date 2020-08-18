""" Workdays without activity report """
from datetime import timedelta, datetime
from report.html_report import HtmlReport
from model.activity import Activity
from util.date_time import is_working_day, get_last_day_of_month


def _short_date(date: datetime) -> str:
    return str(date)[:10]


class WorkdaysWithoutActivityReport(HtmlReport):
    """ Workdays without activity report """
    _REPORT_NAME = "Workdays without activity"

    def __init__(self):
        self._activities = []
        self._dates = []
        self._output = ""

    def _get_html_content(self) -> str:
        self._output = ""
        self._read_activities()
        if len(self._activities) <= 0:
            return "(no activity found)"
        self._build_date_range()
        self._build_output()

        return self._output

    def _get_report_name(self) -> str:
        return self._REPORT_NAME

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

    def _build_output(self):
        self._output += "<table cellspacing=3 cellpadding=3>"
        for date in self._dates:
            workday = is_working_day(date)
            has_activity = self._has_activity_on_date(date)

            self._output += "<tr>"
            if workday:
                self._output += "<td><b>" + _short_date(date) + "</b></td>"
            else:
                self._output += "<td><font color=gray>" + _short_date(date) + "</font></td>"
            self._output += "<td>" + date.strftime("%A") + "</td>"
            self._output += "<td>"
            if workday:
                self._output += "<font color=blue>Workday</font>"
            else:
                self._output += "<font color=gray>Holiday</font>"
            self._output += "</td>"
            self._output += "<td>"
            if workday:
                if has_activity:
                    self._output += "<font color=green>Has activity</font>"
                else:
                    self._output += "<font color=red>No activity</font>"
            else:
                self._output += "-"
            self._output += "</td>"
            self._output += "</tr>"
        self._output += "</table>"

    def _has_activity_on_date(self, date: datetime) -> bool:
        for activity in self._activities:
            if _short_date(activity.date) == _short_date(date):
                return True
        return False

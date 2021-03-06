""" Activity list """
from report.html_report import HtmlReport
from model import activity
from model.activity import Activity
from util import date_time


class ActivityList(HtmlReport):
    """ Activity list """

    _REPORT_NAME = "Activity List"

    def __init__(self):
        self._activities = []
        self._hour_sum = 0

    def _get_activities_of_today(self) -> []:
        output = []
        for act in self._activities:
            if date_time.is_today(act.date):
                output.append(act)
        return output

    def _get_html_content(self) -> str:
        output = ""
        self._read_activities()
        output += self._get_subreport("Today", self._get_activities_of_today())
        output += self._get_subreport("Everything", self._activities)
        return output

    def _get_report_name(self) -> str:
        return self._REPORT_NAME

    def _get_subreport(self, title: str, activities: []) -> str:
        self._hour_sum = 0

        output = ActivityList._get_subtitle(title)
        output += "<table cellspacing=4 cellpadding=4 border=0>"

        output += ActivityList._get_table_line_of_titles()
        for act in activities:
            output += self._get_table_line_of_activity(act)

        output += ActivityList._get_table_line(
            "",
            str(self._hour_sum),
            "∑",
            "",
            ""
        )

        output += "</table>"
        return output

    @staticmethod
    def _get_subtitle(title: str):
        return "<h1>" + title + "</h1>"

    @staticmethod
    def _get_table_line(date: str,
                        hours: str,
                        location: str,
                        project: str,
                        work: str) -> str:
        output = "<tr>"
        output += "<td>" + date + "</td>"
        output += "<td>" + project + "</td>"
        output += "<td>" + location + "</td>"
        output += "<td align=right>" + hours + "</td>"
        output += "<td>" + work + "</td>"
        output += "</tr>"
        return output

    def _get_table_line_of_activity(self, act: activity.Activity) -> str:
        prj = act.project

        output = ActivityList._get_table_line(
            date_time.get_formatted_date(act.date),
            str(act.hours),
            act.location,
            prj.client.name + " - " + prj.name,
            act.work
        )

        self._hour_sum += act.hours
        return output

    @staticmethod
    def _get_table_line_of_titles() -> str:
        return ActivityList._get_table_line(
            "<b>Date</b>",
            "<b>Hours</b>",
            "<b>Location</b>",
            "<b>Project</b>",
            "<b>Work</b>"
        )

    def _read_activities(self):
        self._activities = []

        for act in Activity.get_activities()["activities"]:
            self._activities.append(activity.Activity(act))

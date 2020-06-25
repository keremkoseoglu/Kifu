""" Eczacibasi activity comparison """
from datetime import datetime
from report.html_report import HtmlReport
from util import date_time, ecz_daha
from model.activity import Activity
import config


class EczActivityComparisonLine:
    """ Eczacibasi activity comparison line """

    def __init__(self,
                 p_date: str,
                 p_comment: str,
                 p_ecz_hours: str,
                 p_kifu_hours: str,
                 p_diff_icon: str = ""):
        self.date = p_date
        self.comment = p_comment
        self.ecz_hours = p_ecz_hours
        self.kifu_hours = p_kifu_hours
        self.diff_icon = p_diff_icon


class EczActivityComparison(HtmlReport):
    """ Eczacibasi activity comparison report """

    _REPORT_NAME = "ECZ Activity Comparison"
    _output: str
    _activities: []

    def __init__(self):
        self._output = ""
        self._activities = []

    def _append_comparison_line(self, p_line: EczActivityComparisonLine):
        comment = p_line.comment.replace(",", ",<br>")
        if comment == "":
            comment = "-<br>"

        self._output += "<tr>"
        self._output += "<td align=left valign=top>" + p_line.diff_icon + "</td>"
        self._output += "<td align=left valign=top>" + p_line.date + "</td>"
        self._output += "<td align=right valign=top>" + p_line.ecz_hours + "</td>"
        self._output += "<td align=right valign=top>" + p_line.kifu_hours + "</td>"
        self._output += "<td align=left valign=top>" + comment + "<hr></td>"
        self._output += "</tr>"

    def _get_html_content(self) -> str:
        self._output = ""

        this_year = datetime.now().year
        this_month = datetime.now().month
        self._fill_output_for_month(p_year=this_year, p_month=this_month)

        prev_year = this_year
        prev_month = this_month - 1
        if prev_month == 0:
            prev_year -= 1
            prev_month = 12
        self._fill_output_for_month(p_year=prev_year, p_month=prev_month)

        return self._output

    def _fill_output_for_month(self, p_year: int, p_month: int):
        self._output += "<h1>" + str(p_year) + " " + str(p_month) + "</h1>"
        self._output += "<table cellspacing=3 cellpadding=3 border=0>"

        line = EczActivityComparisonLine(p_date="Tarih",
                                         p_ecz_hours="Eczacıbaşı",
                                         p_kifu_hours="Kifu",
                                         p_comment="Eczacıbaşı yorum",
                                         p_diff_icon="Fark")
        self._append_comparison_line(line)

        sap_year = str(p_year)
        sap_month = date_time.get_two_digit_month(p_month)
        ecz_activities = ecz_daha.get_monthly_activity(p_sap_year=sap_year, p_sap_month=sap_month)

        for ecz_activity in ecz_activities:
            date_of_activity = date_time.parse_sap_date(ecz_activity["date"])

            kifu_hour_sum = Activity.get_time_sum(
                client_name=config.CONSTANTS["COMPANY_NAME_ECZ_TUG"],
                date=date_of_activity)

            diff_icon = "✅"

            if kifu_hour_sum != ecz_activity["hours"]:
                diff_icon = "🔴"

            line = EczActivityComparisonLine(p_date=ecz_activity["date"],
                                             p_comment=ecz_activity["comment"],
                                             p_ecz_hours=str(ecz_activity["hours"]),
                                             p_kifu_hours=str(kifu_hour_sum),
                                             p_diff_icon=diff_icon)

            self._append_comparison_line(line)

        self._output += "</table>"

    def _get_report_name(self) -> str:
        return self._REPORT_NAME

""" HTML report abstract module """
from abc import ABC, abstractmethod
import os
from datetime import datetime
from shutil import copyfile
import config


class HtmlReport(ABC):
    """ Abstract class for HTML based reports """

    _EXTENSION = "html"
    _REPORT_DIR = "report"
    _CHART_FILE = "Chart.min.js"

    def execute(self):
        """ Creates & opens the report """
        complete_html_content = \
            HtmlReport._get_html_prefix() +\
            self._get_html_content() +\
            HtmlReport._get_html_suffix()

        file_path = self._get_file_path()

        with open(file_path, "w") as report_file:
            report_file.write(complete_html_content)

        chart_src = os.path.join(os.getcwd(), HtmlReport._REPORT_DIR, HtmlReport._CHART_FILE)
        chart_tar = os.path.join(config.CONSTANTS["DOWNLOAD_DIR"], HtmlReport._CHART_FILE)
        copyfile(chart_src, chart_tar)

        os.system("open \"" + file_path + "\"")

    @abstractmethod
    def _get_html_content(self) -> str:
        pass

    @abstractmethod
    def _get_report_name(self) -> str:
        pass

    def _get_file_name(self) -> str:

        return \
            self._get_report_name() +\
            " - " +\
            datetime.now().isoformat() +\
            "." +\
            self._EXTENSION

    def _get_file_path(self) -> str:
        return os.path.join(config.CONSTANTS["DOWNLOAD_DIR"], self._get_file_name())

    @staticmethod
    def _get_html_prefix() -> str:
        output = "<html>"
        output += "<head>"
        output += "<script src='Chart.min.js'></script>"
        output += "</head><body>"
        return output

    @staticmethod
    def _get_html_suffix() -> str:
        output = "</body></html>"
        return output

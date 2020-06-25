""" HTML report abstract module """
from abc import ABC, abstractmethod
import os
from datetime import datetime
import config


class HtmlReport(ABC):
    """ Abstract class for HTML based reports """

    _EXTENSION = "html"

    def execute(self):
        """ Creates & opens the report """
        complete_html_content = \
            HtmlReport._get_html_prefix() +\
            self._get_html_content() +\
            HtmlReport._get_html_suffix()

        file_path = self._get_file_path()

        with open(file_path, "w") as report_file:
            report_file.write(complete_html_content)

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
        return output

    @staticmethod
    def _get_html_suffix() -> str:
        output = "</html>"
        return output

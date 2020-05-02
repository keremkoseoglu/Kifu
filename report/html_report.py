from abc import ABC, abstractmethod
from config.constants import *
import os
from datetime import datetime

class HtmlReport(ABC):

    _EXTENSION = "html"

    def __init__(self):
        pass

    def execute(self):
        complete_html_content = \
            self._get_html_prefix() +\
            self._get_html_content() +\
            self._get_html_suffix()

        file_path = self._get_file_path()

        with open(file_path, "w") as f:
            f.write(complete_html_content)

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
        return os.path.join(DOWNLOAD_DIR, self._get_file_name())

    def _get_html_prefix(self) -> str:
        output = "<html>"
        return output

    def _get_html_suffix(self) -> str:
        output = "</html>"
        return output
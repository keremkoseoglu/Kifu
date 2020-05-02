import os
import tkinter
import tkinter.filedialog
import webbrowser
from typing import List


def popup_email(recipients: List[str] = None, subject: str = None, body: str = None, attachment: str = None):
    if recipients is None:
        _recipients = []
    else:
        _recipients = recipients

    if subject is None:
        _subject = ""
    else:
        _subject = subject

    if body is None:
        _body = ""
    else:
        _body = body

    recipient_csv = ""
    for recipient in _recipients:
        if recipient_csv != "":
            recipient_csv += ","
        recipient_csv += recipient

    command = "mailto:?to=" + recipient_csv + "&subject=" + _subject + "&body=" + _body
    webbrowser.open(command, new=1)

    if attachment is not None and attachment != "":
        folder, file = os.path.split(attachment)
        os.system("open " + folder)


def popup_open_file() -> str:
    root = tkinter.Toplevel()
    root.withdraw()
    return tkinter.filedialog.askopenfilename()

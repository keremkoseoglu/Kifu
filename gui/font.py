""" font module """
from tkinter.ttk import Style
import config

def default_font() -> tuple:
    """ Default font """
    return (config.CONSTANTS["GUI_FONT"], config.CONSTANTS["GUI_FONT_SIZE"])

def configure_treeview_style():
    """ Configure tree view style """
    style = Style()
    style.configure("Treeview", font=default_font(), rowheight=config.CONSTANTS["GUI_CELL_HEIGHT"])
    style.configure("Treeview.Heading", font=default_font())

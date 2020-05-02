import os
from config.constants import *


def get_data_file_list() -> []:
    return get_files_in_dir(DATA_DIR_PATH)


def get_desktop_path():
    return os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')


def get_desktop_file_name(file_name: str, extension: str) -> str:
    output = os.path.join(get_desktop_path(), file_name + "." + extension)
    return output


def get_files_in_dir(dir_name: str) -> []:
    output = []

    for current_item in os.listdir(dir_name):
        current_path = os.path.join(dir_name, current_item)
        try:
            if os.path.isfile(current_path) and DATA_FILE_EXTENSION in current_item:
                output.append(current_item)
        except Exception as e:
            print(e)

    output.sort()
    return output


def open_file(path: str):
    if path is None or path == "":
        return
    os.system("open " + path)

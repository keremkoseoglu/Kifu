""" File system utilities """
import os
import config


def get_data_file_list() -> []:
    """ Data file list """
    return get_files_in_dir(config.CONSTANTS["DATA_DIR_PATH"])


def get_desktop_path():
    """ Desktop path """
    return os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')


def get_desktop_file_name(file_name: str, extension: str) -> str:
    """ Desktop file name """
    output = os.path.join(get_desktop_path(), file_name + "." + extension)
    return output


def get_files_in_dir(dir_name: str) -> []:
    """ Returns all files in the given dir """
    output = []

    for current_item in os.listdir(dir_name):
        current_path = os.path.join(dir_name, current_item)
        try:
            if os.path.isfile(current_path) and \
                config.CONSTANTS["DATA_FILE_EXTENSION"] in current_item and \
                "currency_conv_" not in current_item:
                output.append(current_item)
        except Exception as error:
            print(error)

    output.sort()
    return output


def open_file(path: str):
    """ Opens file """
    if path is None or path == "":
        return
    os.system("open " + path)

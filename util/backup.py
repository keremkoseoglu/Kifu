import datetime, os, shutil
from config.constants import *


def clear_old_backups():
    subfolder_path = [f.path for f in os.scandir(_get_root_backup_dir()) if f.is_dir()]
    subfolder_name = [f.name for f in os.scandir(_get_root_backup_dir()) if f.is_dir()]
    deletable_paths = []

    earliest_preservable_date = datetime.datetime.now() - datetime.timedelta(days=BACKUP_PRESERVE_DAYS)

    list_pos = 0
    for name in subfolder_name:
        if _get_date_in_name(name) < earliest_preservable_date:
            deletable_paths.append(subfolder_path[list_pos])
        list_pos += 1

    for path in deletable_paths:
        shutil.rmtree(path)


def execute():
    # Create new directory
    backup_dir = os.path.join(_get_root_backup_dir(), _get_dir_name())
    os.makedirs(backup_dir)

    # Copy files
    for data_file in os.listdir(DATA_DIR_PATH):
        data_file_path = os.path.join(DATA_DIR_PATH, data_file)
        if os.path.isfile(data_file_path):
            shutil.copy(data_file_path, backup_dir)


def _get_date_in_name(name: str) -> datetime.datetime:
    fragments = name.split("-")
    year = int(fragments[0])
    month = int(fragments[1])

    day_frag = fragments[2].split("T")
    day = int(day_frag[0])

    return datetime.datetime(
        year=year,
        month=month,
        day=day
    )


def _get_root_backup_dir() -> str:
    return os.path.join(DATA_DIR_PATH, BACKUP_DIR_PATH)


def _get_dir_name() -> str:
    output = datetime.datetime.now().isoformat()
    output = output.replace(":", "")
    output = output.replace(".", "")
    return output
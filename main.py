""" Main module """
import sys
from gui.prime import Prime
from model import payment
from util import backup
import config


if __name__ == "__main__":
    config.read_constants()
    backup.clear_old_backups()
    if "-test" in sys.argv:
        config.test_mode()
    payment.generate_high_time_recurrences()
    Prime()

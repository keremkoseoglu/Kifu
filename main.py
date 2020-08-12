""" Main module """
import sys
from gui.prime import Prime
from model import payment
from util import backup, currency_update
import config


if __name__ == "__main__":
    config.read_constants()
    backup.clear_old_backups()

    if "-test" in sys.argv:
        config.test_mode()

    payment.generate_high_time_recurrences()

    if config.CONSTANTS["UPDATE_CURRENCIES_ON_STARTUP"]:
        currency_update.execute()

    Prime()

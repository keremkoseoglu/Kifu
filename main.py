""" Main module """
import sys
import datetime
from gui.prime import Prime
from gui.prime_singleton import PrimeSingleton
from model import payment
from model.activity import Activity
from util import backup, currency_update, date_time
import config

def startup():
    """ Main startup function """
    config.read_constants()
    backup.clear_old_backups()

    if "-test" in sys.argv:
        config.test_mode()

    payment.generate_high_time_recurrences()

    if config.CONSTANTS["UPDATE_CURRENCIES_ON_STARTUP"]:
        currency_update.execute()

    add_activity = all([
        date_time.is_working_day(datetime.datetime.now()),
        not Activity.has_activity_for_today()
    ])

    prime = Prime(add_activity=add_activity)
    PrimeSingleton.set(prime)
    prime.start()

if __name__ == "__main__":
    startup()

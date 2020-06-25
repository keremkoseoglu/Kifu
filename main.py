""" Main module """
from gui.prime import Prime
from model import payment
from util import backup
import config


config.read_constants()
backup.clear_old_backups()
payment.generate_high_time_recurrences()
Prime()

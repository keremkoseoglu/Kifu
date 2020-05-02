from gui.prime import Prime
from model import payment
from util import backup

backup.clear_old_backups()
payment.generate_high_time_recurrences()

"""try:
    hosts.overwrite_host_file()
except:
    pass"""

Prime()

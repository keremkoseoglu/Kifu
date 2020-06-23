""" Hosts """
from shutil import copy
from config.constants import HOSTS_FROM, HOSTS_TO

def overwrite_host_file():
    """ Override hosts file """
    copy(HOSTS_FROM, HOSTS_TO)

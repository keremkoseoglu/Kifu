""" Hosts """
from shutil import copy
import config


def overwrite_host_file():
    """ Override hosts file """
    copy(config.CONSTANTS["HOSTS_FROM"], config.CONSTANTS["HOSTS_TO"])

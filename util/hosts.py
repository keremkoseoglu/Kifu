""" Hosts """
from shutil import copy


def overwrite_host_file():
    """ Override hosts file """
    copy("/Users/kerem/OneDrive/etc/config/hosts", "/private/etc/hosts")

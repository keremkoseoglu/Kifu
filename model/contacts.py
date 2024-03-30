""" Mac contacts module """
import os

def test_contacts():
    """ Simple test """
    print(get_address("Dr. Kerem", "Koseoglu"))
    print(get_phone("Dr. Kerem", "Koseoglu"))

def get_address(name: str, surname: str) -> str:
    """ Returns the address of given person
    osascript -e "tell application \"Contacts\" to get formatted address
    of address of first person whose first name is \"Dr. Kerem\" and last name is \"Koseoglu\""
    """
    cmd = 'osascript -e "tell application \\\"Contacts\\\" to get formatted address'
    cmd += ' of address of first person whose first name is \\\"'
    cmd += name
    cmd += '\\\" and last name is \\\"'
    cmd += surname
    cmd += '\\\""'

    return _run_cmd(cmd)

def get_phone(name: str, surname: str) -> str:
    """ Returns the phone of given person """
    cmd = 'osascript -e "tell application \\\"Contacts\\\" to get value of phone'
    cmd += ' of first person whose first name is \\\"'
    cmd += name
    cmd += '\\\" and last name is \\\"'
    cmd += surname
    cmd += '\\\""'

    return _run_cmd(cmd)

def get_email(name: str, surname: str) -> str:
    """ Returns the E-Mail of given person """
    cmd = 'osascript -e "tell application \\\"Contacts\\\" to get value of email'
    cmd += ' of first person whose first name is \\\"'
    cmd += name
    cmd += '\\\" and last name is \\\"'
    cmd += surname
    cmd += '\\\""'

    return _run_cmd(cmd)

def _run_cmd(cmd: str) -> str:
    result = os.popen(cmd).read()
    result = result.replace("\n", " ")
    result = result.replace("  ", " ")
    return result

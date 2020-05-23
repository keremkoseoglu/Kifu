""" GUID """
import uuid

def get_guid() -> str:
    """ Returns a new guid """
    return uuid.uuid4().hex

import datetime
import sys


def info(message):
    """Flush message to console"""
    print(f"{datetime.datetime.now():%Y%m%d-%H%M%S} INFO: {message}")
    sys.stdout.flush()

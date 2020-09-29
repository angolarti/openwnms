import math
import time
from ipaddress import ip_address

from openwnms.domain import Collection


class Struct(Collection):

    def __init__(self, **entries):
        try:
            self.__dict__.update(entries)
        except AttributeError:
            pass


def convert_int_to_time(time_str: str) -> str:

    if time_str == 'NOSUCHINSTANCE' or time_str == 'NOSUCHOBJECT':
        return 0

    return time.strftime('%H:%M:%S', time.gmtime(int(time_str)))


def is_ip_address(ip_addr: str) -> bool:
    try:
        return ip_address(ip_addr) is not None
    except ValueError:
        return False


def convert_units(num_str: str):
    """
    this function will convert bytes to MB.... GB.... TB.... etc
    """
    if num_str == 'NOSUCHINSTANCE' or num_str == 'NOSUCHOBJECT':
        return 0

    step_unit = 1024.0  # 1024 bad the size
    num = int(num_str)

    for unit in ['KB', 'MB', 'GB', 'TB']:
        if num < step_unit:
            return "%d %s" % (math.ceil(num), unit)
        num /= step_unit

from datetime import datetime
from typing import List

from openwnms.domain.repository import Collection


class Hardware(Collection):

    def __init__(self, name: str, kind: str, model: str, manufacturer: str):
        self.name = name
        self.kind = kind
        self.model = model
        self.manufacturer = manufacturer


class Software(Collection):
    def __init__(self, name: str, oldest: str, latest: str, installs: str):
        self.name = name
        self.oldest = oldest
        self.latest = latest
        self.installs = installs


class Device(Collection):

    def __init__(self, hostname: str = None, ip_addr: str = None, mac_addr: str = None, system_operation: str = None,
                 open_ports: List[int] = None, description: str = None, manufacturer: str = None, model: str = None,
                 owner: str = None, purchase_price: float = None, location: str = None, last_update_time: datetime = None,
                 last_scan_time: datetime = None, groups: List[str] = None, hardware: List[Hardware] = None,
                 software: List[Software] = None):
        self.hostname = hostname
        self.ip_addr = ip_addr
        self.mac_addr = mac_addr
        self.system_operation = system_operation
        self.open_ports = open_ports
        self.description = description
        self.manufacturer = manufacturer
        self.model = model
        self.owner = owner
        self.purchase_price = purchase_price
        self.location = location
        self.last_update_time = last_update_time
        self.last_san_time = last_scan_time
        self.groups = groups
        self.hardware = hardware
        self.software = software


if __name__ == '__main__':
    hr = Hardware('RAM', 'Memory', 'DDR2', 'VT')

    print(hr.to_collection())
    print(hr.__class__.__name__.lower())

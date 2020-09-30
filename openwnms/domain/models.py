from datetime import datetime

from openwnms.domain.repository import Collection


class SystemInfo(Collection):

    def __init__(self, **entries):
        self.__dict__.update(entries)


class Device(Collection):

    def __init__(self, hostname: str = None, ip_addr: str = None, mac_addr: str = None, description: str = None,
                 manufacturer: str = None, model: str = None, owner: str = None, purchase_price: float = None,
                 location: str = None, last_update_time: datetime = datetime.now(),
                 last_scan_time: datetime = datetime.now(), created_at: datetime = None):
        super().__init__()
        self.hostname = hostname
        self.ip_addr = ip_addr
        self.mac_addr = mac_addr
        self.description = description
        self.manufacturer = manufacturer
        self.model = model
        self.owner = owner
        self.purchase_price = purchase_price
        self.location = location
        self.last_update_time = last_update_time
        self.last_san_time = last_scan_time
        self.created_at = created_at

    class build:
        pass


if __name__ == '__main__':
    pass

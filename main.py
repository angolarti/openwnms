from datetime import datetime

from openwnms.domain.models import Device, SystemInfo
from openwnms.domain.services import ScanDevice
from openwnms.infrastructure.subsystem.snmp.collector import MIB
from openwnms.tools.utils import get_ipv4_addr, conf


def save_collection(target_mib: str, device_scan: SystemInfo, status: bool = False) -> dict:

    disk_statistics = []
    device: Device = Device()
        
    if target_mib:
        device.hostname = device_scan.hostname
        device.ip_addr = device_scan.ip_addr
        device.mac_addr = device_scan.mac_addr
        device.system_info = target_mib.system_info
        for _, disk_statistic in target_mib.disk_statistics.items():
            disk_statistics.append(disk_statistic)
        device.disk_statistics = disk_statistics
        device.memory_statistics = target_mib.memory_statistics
        device.cpu_statistics = target_mib.cpu_statistics
        device.cpu_times = target_mib.cpu_times
        device.created_at = datetime.now()
        if not status:
            device.save()
        else:
            device._id = device_scan._id
            device.update()

        return device.to_collection()


def scan():
    print('Starting...')
    devices = []
    all_address = list(range(11))
    
    _address = [1, 22, 27, 30, 44, 92, 104, 112, 148, 191, 225]
    
    net_scan_devices = ScanDevice.net_discovery_host(all_address)
    ScanDevice.net_scan_ifaces()

    for reply in net_scan_devices:
        try:
            ScanDevice.net_scan_device(reply.src)
        except AttributeError:
            pass

    ScanDevice.net_scan_device(get_ipv4_addr(conf.iface))
    network_devices = ScanDevice.show_network_devices()
 
    for key, value in network_devices.items():
        if not isinstance(value, int):
            device = SystemInfo(**network_devices[key])
            target_host_mib = MIB(device.ip_addr)
            find_device = Device().find_by_mac_addr(device.mac_addr)
            print(f'Scanned: {target_host_mib}')
            if find_device is None:
                devices.append(save_collection(target_host_mib, device))
            else:
                device._id = find_device['_id']
                devices.append(save_collection(target_host_mib, device, True))
    
    return devices


if __name__ == '__main__':
    scan()

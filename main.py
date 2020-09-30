from datetime import datetime

from openwnms.domain.models import Device, SystemInfo
from openwnms.domain.services import ScanDevice
from openwnms.infrastructure.subsystem.snmp.collector import MIB
from openwnms.tools.utils import get_ipv4_addr, conf


def save_collection(target_mib: str, device_scan: SystemInfo) -> dict:

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
        device.save()

        return device.to_collection()


if __name__ == '__main__':

    net_scan_devices = ScanDevice.net_discovery_host()
    ScanDevice.net_scan_ifaces()

    for reply in net_scan_devices:
        try:
            ScanDevice.net_scan_device(reply.src)
        except AttributeError:
            pass

    ScanDevice.net_scan_device(get_ipv4_addr(conf.iface))

    network_devices = ScanDevice.show_network_devices()
    print(network_devices)

    for key, value in network_devices.items():
        if not isinstance(value, int):
            device = SystemInfo(**network_devices[key])
            print(device.hostname)
            target_host_mib = MIB(device.ip_addr)
            print('Host: ', Device().find_by_mac_addr(device.mac_addr))
            if Device().find_by_mac_addr(device.mac_addr) is None:
                print(save_collection(target_host_mib, device))
            else:
                print('Device exists: ', device.hostname)
    print('-----------------------------------------------')

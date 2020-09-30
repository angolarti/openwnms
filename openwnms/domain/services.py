from openwnms.tools.utils import network_scanner, get_ipv4_addr, get_ipv6_addr, get_hostname, \
    get_all_ifaces, get_mac_addr, conf, get_mac_by_ip


class ScanDevice:
    __NET_SOURCE = get_ipv4_addr(conf.iface)
    __NET_TARGET = __NET_SOURCE[:len(__NET_SOURCE) - 3]
    __network_devices = {
        'total_online': 0,
        'total_offline': 0
    }
    __network_interfaces = {}

    @staticmethod
    def net_discovery_host(start: int = 1, end: int = 256):
        return network_scanner(ScanDevice.__NET_TARGET, start, end)

    @staticmethod
    def net_scan_device(target):

        if not (target is None):
            ScanDevice.__build_dict_device_scan(target)
            ScanDevice.__network_devices['total_online'] += 1
        else:
            ScanDevice.__network_devices['total_offline'] += 1

    @staticmethod
    def __build_dict_device_scan(target):

        ScanDevice.__network_devices[target] = {
            'hostname': get_hostname(target),
            'ip_addr': target,
            'mac_addr': get_mac_by_ip(target)
        }


    @staticmethod
    def net_scan_ifaces():
        for iface in get_all_ifaces():
            ScanDevice.__network_interfaces[iface] = {
                'mac_addr': get_mac_addr(iface),
                'ipv4_addr': get_ipv4_addr(iface),
                'ipv6_addr': get_ipv6_addr(iface),
            }

    @staticmethod
    def show_network_devices():
        return ScanDevice.__network_devices

    @staticmethod
    def show_host_interfaces_info():
        return ScanDevice.__network_interfaces


if __name__ == '__main__':

    net_scan_devices = ScanDevice.net_discovery_host(1, 25)
    ScanDevice.net_scan_ifaces()

    for reply in net_scan_devices:
        ScanDevice.net_scan_device(reply)

    print(ScanDevice.show_network_devices())
    print(ScanDevice.show_host_interfaces_info())

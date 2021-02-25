from datetime import datetime, date, timedelta
import socket
from scapy.all import (
    IP, ICMP, conf, getmacbyip, sr1, srp, Ether, ARP, get_if_addr, get_if_hwaddr, get_if_list, get_if_addr6
)
import logging
import scapy.error

logging.getLogger('scapy.runtime').setLevel(logging.ERROR)

TIMEOUT = 2
conf.verb = 0


def network_scanner(net_target: str, address) -> list:

    print('Start scanner...')
    network_devices: list = []
    for ip in range(0, len(address)):
        print(f'start here: {ip}',)
        packet = IP(dst=f'{net_target}.{address[ip]}', ttl=20) / ICMP()
        try:
            print(f'Found : {sr1(packet, timeout=TIMEOUT).src}')
            network_devices.append(sr1(packet, timeout=TIMEOUT))
        except AttributeError:
            print(f'Not Found : {net_target}.{address[ip]}')
            continue

    return network_devices


def ping(ip: str) -> bool:
    packet = IP(dst=ip) / ICMP()
    reply = sr1(packet, timeout=TIMEOUT)
    return not (reply is None)


def get_ipv4_addr(iface):
    return get_if_addr(iface)


def get_ipv6_addr(iface):
    return get_if_addr6(iface)


def get_mac_addr(iface):
    try:
        return get_if_hwaddr(iface)
    except (OSError, scapy.error.Scapy_Exception):
        pass


def get_mac_by_ip(ip: str):
    return getmacbyip(ip)


def get_hostname(ip: str):
    return socket.getfqdn(ip)


def get_all_ifaces():
    return get_if_list()


def last_five_days(current_datetime):
    return current_datetime - timedelta(5)


def current_datetime():
    return datetime.today()


if __name__ == '__main__':
    print('Current Date :', current_datetime())
    print('5 days before Current Date :', last_five_days(current_datetime()))
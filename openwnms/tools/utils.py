import socket

from scapy.all import (
    IP, ICMP, conf, getmacbyip, sr1, srp, Ether, ARP, get_if_addr, get_if_hwaddr, get_if_list, get_if_addr6
)
import logging

logging.getLogger('scapy.runtime').setLevel(logging.ERROR)

TIMEOUT = 2
conf.verb = 0


def scanner(net_target: str) -> dict:
    network_devices = {
        'total_online': 0,
        'total_offline': 0
    }
    print('Start scanner...')

    for ip in range(0, 256):
        packet = IP(dst=f'{net_target}.{ip}', ttl=20) / ICMP()
        reply = sr1(packet, timeout=TIMEOUT)

        if not (reply is None):
            network_devices[reply.src] = {
                'hostname': socket.getfqdn(reply.src),
                'mac_addr': getmacbyip(reply.src)
            }
            network_devices['total_online'] += 1

        else:
            network_devices['total_offline'] += 1

    return network_devices


def is_online(ip: str) -> bool:
    packet = IP(dst=ip, ttl=20) / ICMP()
    reply = sr1(packet, timeout=TIMEOUT)
    return not (reply is None)


def get_ipv4_addr():
    return get_if_addr(conf.iface)


def get_ipv6_addr():
    return get_if_addr6(conf.iface)


def get_mac_addr():
    return get_if_hwaddr(conf.iface)


def show_network_info():
    network_interfaces = {}

    for iface in get_if_list():
        network_interfaces[iface] = {
            'mac_addr': get_if_hwaddr(iface),
            'ipv4_addr': get_if_addr(iface),
            'ipv6_addr': get_if_addr6(iface),
        }
    return network_interfaces


if __name__ == '__main__':
    net_source = get_ipv4_addr()
    net_target = net_source[:len(net_source) - 3]

    print(is_online('192.168.0.100'))
    print(scanner(net_target))

    print(get_ipv4_addr())
    print(get_mac_addr())

    print(show_network_info())

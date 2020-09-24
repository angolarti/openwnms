import logging
import socket

import scapy.all as scapy


logging.getLogger('scapy.runtime').setLevel(logging.ERROR)


class Network(object):

    @staticmethod
    def icmp_scan(ip_addr: str):
        """
        :param ip_addr: XXX.XXX.XXX.XXX
        :return: ip_addr, mac_addr, hostname
        """

        ans = scapy.sr(scapy.IP(dst=f'{ip_addr}') / scapy.ICMP(),
                       timeout=1, verbose=0)  # send and receive packet in layer 3
        if ans[0]:
            try:
                return ans[0].res[0][0].dst, scapy.getmacbyip(ans[0].res[0][0].dst), \
                       socket.getfqdn(ans[0].res[0][0].dst)
            except (socket.herror, AttributeError, IndexError) as error:
                pass

    @staticmethod
    def port_scan(ip_addr: str, port_start: int, port_end: int = None):
        ports = []
        if port_end is not None:
            for port in range(port_start, port_end):
                response = scapy.sr1(scapy.IP(dst=f'{ip_addr}')/scapy.TCP(dport=port, flags='S'), verbose=0)
                result = response['TCP'].flags
                if result == 18:
                    ports.append(port)
                else:
                    continue
        return ports


class Loopback:

    @staticmethod
    def get_if_list():
        return scapy.get_if_list()

    @staticmethod
    def get_ip_addr(iff):
        return scapy.get_if_addr(iff)


if __name__ == '__main__':

    print(f'Ifaces: {Loopback.get_if_list()}')
    print(f'IP: {Loopback.get_ip_addr(Loopback.get_if_list()[1])}')

    ip_range = ['192.168.0.1', '192.168.0.100']
    first_ip_addr = ip_range[0].split('.')
    last_ip_addr = ip_range[len(ip_range)-1].split('.')

    net_addr = f'{first_ip_addr[0]}.{first_ip_addr[1]}.{first_ip_addr[2]}'
    for addr in range(int(first_ip_addr[3]), int(last_ip_addr[3])+1):
        try:
            ip =  f'{net_addr}.{addr}'
            ip_addr, mac_addr, hostname = Network.icmp_scan(ip)
            print(f'IP ADDR: {ip_addr}, MAC ADDR: {mac_addr} Hostname: {hostname}')
            # print(f'Open ports: {Network.port_scan(ip, 22, 25)}')
        except TypeError:
            continue

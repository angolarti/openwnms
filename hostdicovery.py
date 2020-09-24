import socket

import scapy.all as scapy
import logging


logging.getLogger('scapy.runtime').setLevel(logging.ERROR)

addr_const = '192.168.0.'
dst = None

for addr in range(1, 2):
    ans = scapy.sr(scapy.IP(dst='192.168.0.16')/scapy.ICMP(),
                   timeout=5, verbose=0)  # send and receive packet in layer 3
    if ans[0]:
        try:
            print(f'[+] Host is up {ans[0].res[0][0].dst} '
                  f'MAC: {scapy.getmacbyip(ans[0].res[0][0].dst)} '
                  f'Qualified hostname: {socket.getfqdn(ans[0].res[0][0].dst)} ')
        except (socket.herror, AttributeError, IndexError) as error:
            print(error)
            continue

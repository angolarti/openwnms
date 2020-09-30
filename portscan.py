from scapy.all import *


for port in range(1, 1025):
    resposta = sr1(IP(dst='192.168.0.1')/TCP(dport=port, flags='S'), verbose=0)
    result = resposta['TCP'].flags
    if result == 18:
        print(f'Porta {port} aberta')
    else:
        continue
    #print(resposta.show())
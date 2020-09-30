import nmap

scanner = nmap.PortScanner()

print('Welcome, this is a simple nmap automation tool')
print('<-------------------------------------------------->')

ip_addr = input('Please enter the IP adrress you want to scan: ')
print('The IP you entered is: ', ip_addr)
type(ip_addr)

response = input("""\nPlease entre the type of scan yu want to run
                    1) SYN ACK Scan
                    2) UDP Scan
                    3) Comprehensive Scan \n""")
print('You have selected option: ', response)

if response == '1':
    print("Nmap Version: ", scanner.nmap_version())
    scanner.scan(ip_addr, '1-1024', '-v -sS')
    print(scanner.scaninfo())
    print('Ip Status: ', scanner[ip_addr].state())
    print('Protocols:', scanner[ip_addr].all_protocols())
    print('Open Ports: ', scanner[ip_addr]['tcp'].keys())
    print('All: ', scanner[ip_addr])
elif response == '2':
    print("Nmap Version: ", scanner.nmap_version())
    scanner.scan(ip_addr, '1-1024', '-v -sU')
    print(scanner.scaninfo())
    print('Ip Status: ', scanner[ip_addr].state())
    print('Protocols:', scanner[ip_addr].all_protocols())
    print('Open Ports: ', scanner[ip_addr]['udp'].keys())
    print('All: ', scanner[ip_addr])
elif response == '3':
    print("Nmap Version: ", scanner.nmap_version())
    scanner.scan(ip_addr, '1-1024', '-v -sS -sV -sC -A -O')
    print(scanner.scaninfo())
    print('Ip Status: ', scanner[ip_addr].state())
    print('Protocols:', scanner[ip_addr].all_protocols())
    print('Open Ports: ', scanner[ip_addr]['tcp'].keys())
    print('All: ', scanner[ip_addr])
elif response == '4':
    print('Please enter a valid option')

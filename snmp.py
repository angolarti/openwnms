from datetime import datetime

from easysnmp import Session
import scapy.all as scapy

from openwnms.infrastructure.subsystem.snmp.collector import MIB
from openwnms.domain.models import Device, SystemInfo
from utils import convert_units, Struct


def get_system_info(session):

    def get_version_distribution(description):
        """
        :param description:
        :return: dist_name, dist_version, kernel_name, kernel_version, hostname
        """
        try:
            if description[3] != '#1' and description[0] == 'Linux':
                distribution = description[3].split('-')
                return {
                    'distribution_name': distribution[1],
                    'distribution_version': distribution[0].split('~')[1],
                    'operating_system': description[0],
                    'operating_system_version': description[2].split('-')[0],
                    'architecture': description[len(description)-1]
                }
            elif 'Windows' == description[12]:
                return {
                    'operating_system': description[12],
                    'operating_system_version': description[14],
                    'architecture': description[1]
                }
            return {
                'distribution_name': description[2].split('-')[2],
                'distribution_version': description[2].split('-')[1],
                'operating_system': description[0],
                'operating_system_version': description[2].split('-')[0],
                'architecture': description[len(description) - 1]
            }
        except IndexError:
            pass

    try:
        description = session.get('sysDescr.0').value.split(' ')
        return SystemInfo(**get_version_distribution(description))
    except (SystemError, TypeError) as error:
        print(error)


NO_SUCH_OBJECT = 'NOSUCHOBJECT'
NO_SUCH_INSTANCE = 'NOSUCHINSTANCE'


class MemoryStatistic:

    @staticmethod
    def __calculate_size(session: Session, oid: str):
        cached_ram = session.walk(oid)
        if len(cached_ram):
            if cached_ram == NO_SUCH_INSTANCE or cached_ram == NO_SUCH_OBJECT:
                return NO_SUCH_INSTANCE

            return convert_units(int(cached_ram[0].value))
        return 0


class DiskStatistic:

    @staticmethod
    def __calculate_size(session: Session, oid: str):
        cached_ram = session.get(oid).value
        if cached_ram == NO_SUCH_INSTANCE or cached_ram == NO_SUCH_OBJECT:
            return NO_SUCH_INSTANCE

        return convert_units(int(cached_ram))


def save_collection(target_host_mib: str) -> dict:

    disk_statistics = []
    device: Device = Device()

    if target_host_mib:
        device.ip_addr = host
        device.mac_addr = scapy.getmacbyip(host)
        device.system_info = target_host_mib.system_info
        for _, disk_statistic in target_host_mib.disk_statistics.items():
            disk_statistics.append(disk_statistic)
        device.disk_statistics = disk_statistics
        device.memory_statistics = target_host_mib.memory_statistics
        device.cpu_statistics = target_host_mib.cpu_statistics
        device.cpu_times = target_host_mib.cpu_times
        device.created_at = datetime.now()
        device.save()

        return device.to_collection()


if __name__ == '__main__':
    # hosts = ['192.168.0.1', '192.168.0.11', '192.168.0.12', '192.168.0.14', '192.168.0.15']
    hosts = ['192.168.0.12', '192.168.0.15', '192.168.0.16', '192.168.0.18', '192.168.0.20', '192.168.0.21']
    for host in hosts:
        target_host_mib = MIB(host)
        print(save_collection(target_host_mib))
    print('-----------------------------------------------')

from easysnmp import Session
import scapy.all as scapy

from utils import convert_int_to_time, convert_units


def connect(hostname: str, community: str = 'public', version: int = 2) -> Session:
    return Session(hostname=hostname, community=community, version=version)


def get_cpu_usage(session):
    try:
        return session.get('ssCpuSystem.0').value
    except SystemError as error:
        print(error)


def get_system_info(session):

    def get_version_distribution(description):
        """
        :param description:
        :return: dist_name, dist_version, kernel_name, kernel_version, hostname
        """
        print(description)
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


def get_hostname(session):
    try:
        return session.get('sysName.0').value
    except SystemError as error:
        print(error)


def get_system_up_time(session):
    try:
        return session.get('sysUpTime.0').value
    except SystemError as error:
        print(error)


def disk_space_free(session: Session):
    try:
        return session.get('.1.3.6.1.4.1.2021.9.1.6.1').value
    except SystemError as error:
        print(error)


def walk(session: Session):
    try:
        system_items = session.walk('system')
        for item in system_items:
            print('{oid}.{oid_index} {snmp_type} = {value}'.format(
                oid=item.oid,
                oid_index=item.oid_index,
                snmp_type=item.snmp_type,
                value=item.value
            ))
    except SystemError as error:
        print(error)


NO_SUCH_OBJECT = 'NOSUCHOBJECT'
NO_SUCH_INSTANCE = 'NOSUCHINSTANCE'


class MemoryStatistic:

    @staticmethod
    def total_swap_size(session: Session):
        try:
            return MemoryStatistic.__calculate_size(session, '.1.3.6.1.4.1.2021.4.3')
        except SystemError as error:
            print(error)

    @staticmethod
    def available_swap_size(session: Session):
        try:
            return MemoryStatistic.__calculate_size(session, 'memAvailSwap.0')
        except SystemError as error:
            print(error)

    @staticmethod
    def total_ram_in_machine(session: Session):
        try:
            return MemoryStatistic.__calculate_size(session, 'UCD-SNMP-MIB::memTotalReal.0 ')
        except SystemError:
            pass

    @staticmethod
    def available_ram_used(session: Session):
        try:
            return MemoryStatistic.__calculate_size(session, 'memAvailReal.0')
        except SystemError:
            pass

    @staticmethod
    def total_ram_free(session: Session):
        try:
            return MemoryStatistic.__calculate_size(session, 'memTotalFree.0')
        except SystemError:
            pass

    @staticmethod
    def total_ram_shared(session: Session):
        try:
            return MemoryStatistic.__calculate_size(session, 'memShared.0')
        except SystemError:
            pass

    @staticmethod
    def total_ram_buffered(session: Session):
        try:
            return MemoryStatistic.__calculate_size(session, 'memBuffer.0')
        except SystemError:
            pass

    @staticmethod
    def total_cached_memory(session: Session):
        try:
            return MemoryStatistic.__calculate_size(session, 'memCached.0')
        except SystemError:
            pass

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
    def disk_storage_capacity(session: Session):
        try:
            return DiskStatistic.__calculate_size(session, 'HOST-RESOURCES-MIB::hrDiskStorageCapacity.393232')
        except SystemError:
            pass

    @staticmethod
    def disk_info(session: Session):
        try:
            return session.bulkwalk('.1.3.6.1.4.1.2021.4')
        except (SystemError, IndexError):
            pass

    @staticmethod
    def __calculate_size(session: Session, oid: str):
        cached_ram = session.get(oid).value
        if cached_ram == NO_SUCH_INSTANCE or cached_ram == NO_SUCH_OBJECT:
            return NO_SUCH_INSTANCE

        return convert_units(int(cached_ram))


class HwStatistic:

    @staticmethod
    def amount_time_host_was_last_initialized(session: Session):
        try:
            return convert_int_to_time(int(session.get('hrSystemUptime.0').value))
        except SystemError:
            pass

    @staticmethod
    def test_oid(session: Session):
        try:
            return session.get('.1.3.6.1.2.1.25.3.8.1.2').value
        except (SystemError, ValueError):
            pass

()
if __name__ == '__main__':

    from openwnms.domain.models import Device, Hardware, Software, SystemInfo

    # hosts = ['192.168.0.1', '192.168.0.11', '192.168.0.12', '192.168.0.14', '192.168.0.15']
    hosts = ['192.168.0.12', '192.168.0.16', '192.168.0.18', '192.168.0.20', '192.168.0.21']

    for host in hosts:

        if get_hostname(connect(host)) is not None:
            for disk in DiskStatistic.disk_info(connect(host)):
                print(disk)
                print('RAM: ', convert_units(int(8006972)))
            print("HOST", host, 'TOTAL SWAP: ', MemoryStatistic.total_swap_size(connect(host)))
            continue

            hardware = {}
            device = Device()

            device.hostname = get_hostname(connect(host))
            device.ip_addr = host
            device.mac_addr = scapy.getmacbyip(host)
            device.system_info = get_system_info(connect(host)).to_collection()

            memory_ram = Hardware('Memory RAM', None, None, MemoryStatistic.total_ram_in_machine(connect(host)))
            memory_ram.total_in_machine = MemoryStatistic.total_ram_in_machine(connect(host))
            memory_ram.cached = MemoryStatistic.total_cached_memory(connect(host))
            memory_ram.shared = MemoryStatistic.total_ram_shared(connect(host))
            memory_ram.buffered = MemoryStatistic.total_ram_buffered(connect(host))
            memory_ram.free = MemoryStatistic.total_ram_free(connect(host))
            memory_ram.available = MemoryStatistic.available_ram_used(connect(host))
            hardware['ram'] = memory_ram.to_collection()

            memory_swap = Hardware('Memory Swap', None, None, MemoryStatistic.total_swap_size(connect(host)))
            memory_swap.available = MemoryStatistic.available_swap_size(connect(host))
            hardware['swap'] = memory_swap.to_collection()

            cpu = Hardware('CPU', None, None, get_cpu_usage(connect(host)))
            hardware['cpu'] = cpu.to_collection()

            disk = Hardware('Disk (HD)', None, None, DiskStatistic.disk_storage_capacity(connect(host)))
            hardware['disk'] = disk.to_collection()

            device.hardware = hardware
            from datetime import datetime
            device.created_at = datetime.now()
            # device.save()

            """print(f'Hostname: {get_hostname(connect(host))}')
            print(f'Total Swap Size: {MemoryStatistic.total_swap_size(connect(host))}')
            print(f'Available Swap Size: {MemoryStatistic.available_swap_size(connect(host))}')
            print(f'Total RAM Size: {MemoryStatistic.total_ram_in_machine(connect(host))}')
            print(f'Available RAM Used: {MemoryStatistic.available_ram_used(connect(host))}')
            print(f'Total RAM Free: {MemoryStatistic.total_ram_free(connect(host))}')
            print(f'Total RAM Shared: {MemoryStatistic.total_ram_shared(connect(host))}')
            print(f'Total RAM Buffered: {MemoryStatistic.total_ram_buffered(connect(host))}')
            print(f'Total Cached Memory: {MemoryStatistic.total_cached_memory(connect(host))}')
            print(f'Disk Size (HDD): {DiskStatistic.disk_storage_capacity(connect(host))}')
            print(f'CPU: {get_cpu_usage(connect(host))}')
            print(f'System operation: {get_system_name(connect(host))[0]}')
            print(f'System arch: {get_system_name(connect(host))[1]}')
            print(f'Up Time: {convert_int_to_time(int(get_system_up_time(connect(host))))}')

            print(f'Amount Time Was Last Initialized: {HwStatistic.amount_time_host_was_last_initialized(connect(host))}')"""
            print(device.to_collection())
        print('-----------------------------------------------')

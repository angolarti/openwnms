from easysnmp import Session
from utils import convert_int_to_time, convert_units


def connect(hostname: str, community: str = 'public', version: int = 2) -> Session:
    return Session(hostname=hostname, community=community, version=version)


def get_cpu_usage(session):
    try:
        return session.get('ssCpuSystem.0').value
    except SystemError as error:
        print(error)


def get_system_name(session):
    try:
        description = session.get('sysDescr.0').value.split(' ')
        return description[2], description[len(description)-1]
    except SystemError as error:
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
            return MemoryStatistic.__calculate_size(session, 'memTotalSwap.0')
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
            return MemoryStatistic.__calculate_size(session, 'memTotalReal.0')
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
        cached_ram = session.get(oid).value
        if cached_ram != NO_SUCH_OBJECT:
            return convert_units(int(cached_ram))

        return NO_SUCH_OBJECT


class DiskStatistic:

    @staticmethod
    def disk_storage_capacity(session: Session):
        try:
            return DiskStatistic.__calculate_size(session, 'HOST-RESOURCES-MIB::hrDiskStorageCapacity.393232')
        except SystemError:
            pass

    @staticmethod
    def __calculate_size(session: Session, oid: str):
        cached_ram = session.get(oid).value
        if cached_ram != NO_SUCH_INSTANCE and cached_ram != NO_SUCH_OBJECT:
            return convert_units(int(cached_ram))

        return NO_SUCH_INSTANCE


class HwStatistic:

    @staticmethod
    def amount_time_host_was_last_initialized(session: Session):
        try:
            return convert_int_to_time(int(session.get('hrSystemUptime.0').value))
        except SystemError:
            pass


if __name__ == '__main__':

    hosts = ['192.168.0.16', '192.168.0.12', '192.168.0.19', '192.168.0.20', '192.168.0.21']

    for host in hosts:
        if get_system_name(connect(host)) is not None:
            print(f'Hostname: {get_hostname(connect(host))}')
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

            print(f'Amount Time Was Last Initialized: {HwStatistic.amount_time_host_was_last_initialized(connect(host))}')
        print('-----------------------------------------------')

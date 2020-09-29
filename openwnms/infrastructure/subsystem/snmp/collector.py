import types

from easysnmp import Session

from openwnms.infrastructure.subsystem.snmp import System
from openwnms.infrastructure.subsystem.snmp.memory import DiskStatistics, MemoryStatistics
from openwnms.infrastructure.subsystem.snmp.processor import CPUStatistic, CPUTimes
from utils import convert_units, convert_int_to_time


class Agent:

    _shared_state = {
    }

    def __new__(cls):
        inst = super().__new__(cls)
        inst.__dict__ = cls._shared_state
        return inst


class MIB:

    def __init__(self, target: str = '127.0.0.1', community: str = 'public', version: int = 2):
        self.agent = Agent()
        self.agent.community = community
        self.agent.version = version
        self.agent.hostname = target

        if target != '127.0.0.1':
            self.agent.hostname = target
        if community != 'public':
            self.agent.community = community
        if version != 2:
            self.agent.version = version

    def collect(self, callable: types.FunctionType):
        """
        :type callable: function
        """
        try:
            snmp_variable = self.__session.walk(callable())
            if len(snmp_variable) == 0:
                return self.__session.get(callable())
            return snmp_variable
        except SystemError:
            pass

    @property
    def __session(self) -> Session:
        try:
            return Session(hostname=self.agent.hostname, version=self.agent.version, community=self.agent.community)
        except SystemError:
            pass

    @property
    def disk_statistics(self):

        disk_statistics = {}

        path_mounts = self.collect(DiskStatistics.path_where_the_disk_is_mounted)
        path_device_for_partitions = self.collect(DiskStatistics.path_of_the_device_for_the_partition)
        total_size_of_disk_or_partitions = self.collect(DiskStatistics.total_size_of_disk_or_partition)
        available_spaces_disk = self.collect(DiskStatistics.available_space_on_the_disk)
        used_spaces_disk = self.collect(DiskStatistics.used_space_on_the_disk)
        percentages_space_used_disk = self.collect(DiskStatistics.percentage_of_space_used_on_disk)
        percentages_space_inodes_disk = self.collect(DiskStatistics.percentage_of_inodes_used_on_disk)

        try:
            for index, path_mounted in enumerate(path_mounts):
                disk_statistics[index] = {'path_mounted': path_mounted.value}

            for index, path_partition in enumerate(path_device_for_partitions):
                disk_statistics[index]['path_partition'] = path_partition.value

            for index, size_of_disk_or_partition in enumerate(total_size_of_disk_or_partitions):
                disk_statistics[index]['size_of_disk_or_partition'] = convert_units(size_of_disk_or_partition.value)

            for index, available_space_disk in enumerate(available_spaces_disk):
                disk_statistics[index]['available_space_disk'] = convert_units(available_space_disk.value)

            for index, used_space_disk in enumerate(used_spaces_disk):
                disk_statistics[index]['used_space_disk'] = convert_units(used_space_disk.value)

            for index, percentage_space_used_disk in enumerate(percentages_space_used_disk):
                disk_statistics[index]['percentage_space_used_disk'] = int(percentage_space_used_disk.value)

            for index, percentage_space_inodes_disk in enumerate(percentages_space_inodes_disk):
                disk_statistics[index]['percentage_space_inodes_disk'] = int(percentage_space_used_disk.value)
        except TypeError:
            try:
                disk_statistics['path_mounted'] = path_mounted.value
                disk_statistics['path_partition'] = path_partition.value
                disk_statistics['size_of_disk_or_partition'] = convert_units(size_of_disk_or_partition.value)
                disk_statistics['available_space_disk'] = convert_units(available_space_disk.value)
                disk_statistics['used_space_disk'] = convert_units(used_space_disk.value)
                disk_statistics['percentage_space_used_disk'] = int(percentage_space_used_disk.value)
                disk_statistics['percentage_space_inodes_disk'] = int(percentage_space_used_disk.value)
            except UnboundLocalError:
                pass

        return disk_statistics

    @property
    def memory_statistics(self):
        try:
            memory_statistics = {
                'total_swap_size': convert_units(self.collect(MemoryStatistics.total_swap_size).value),
                'available_swap_space': convert_units(self.collect(MemoryStatistics.available_swap_space).value),
                'total_ram_in_machine': convert_units(self.collect(MemoryStatistics.total_ram_in_machine).value),
                'total_ram_used': convert_units(self.collect(MemoryStatistics.total_ram_shared).value),
                'total_ram_free': convert_units(self.collect(MemoryStatistics.total_ram_free).value),
                'total_ram_shared': convert_units(self.collect(MemoryStatistics.total_ram_shared).value),
                'total_ram_buffered': convert_units(self.collect(MemoryStatistics.total_ram_buffered).value),
                'total_cached_memory': convert_units(self.collect(MemoryStatistics.total_cached_memory).value)
            }

            return memory_statistics
        except AttributeError:
            pass

    @property
    def cpu_statistics(self):
        try:
            cpu_statistics = {
                'one_minute_load': self.collect(CPUStatistic.one_minute_load).value,
                'five_minute_load': self.collect(CPUStatistic.five_minute_load).value,
                'fifteen_minute_load': self.collect(CPUStatistic.fifteen_minute_load).value
            }
            return cpu_statistics
        except AttributeError:
            pass

    @property
    def cpu_times(self):
        try:
            cpu_times = {
                'percentage_of_user_cpu_time': self.collect(CPUTimes.percentage_of_user_cpu_time).value,
                'raw_user_cpu_time': convert_int_to_time(self.collect(CPUTimes.raw_user_cpu_time).value),
                'percentages_of_system_cpu_time': self.collect(CPUTimes.percentages_of_system_cpu_time).value,
                'raw_system_cpu_time': convert_int_to_time(self.collect(CPUTimes.raw_system_cpu_time).value),
                'percentages_of_idle_cpu_time': self.collect(CPUTimes.percentages_of_idle_cpu_time).value,
                'raw_idle_cpu_time': convert_int_to_time(self.collect(CPUTimes.raw_idle_cpu_time).value),
                'raw_nice_cpu_time': convert_int_to_time(self.collect(CPUTimes.raw_nice_cpu_time).value),
            }
            return cpu_times
        except AttributeError:
            pass

    @property
    def system_info(self):
        try:
            return {
                'system_uptime': convert_int_to_time(int(self.collect(System.system_uptime).value)),
                'total_processes': self.collect(System.total_processes)[0].value,
                'amount_time_host_was_last_initialized': convert_int_to_time(
                    int(self.collect(System.amount_time_host_was_last_initialized)[0].value)),
                'system_operation': self.collect(System.system_description).value,
                'hostname': self.collect(System.get_hostname).value
            }
        except AttributeError:
            pass


if __name__ == '__main__':
    print('Memory: ', MIB('192.168.0.16').memory_statistics)
    print('Disk: ', MIB('192.168.0.16').disk_statistics)
    print('CPU Statistic: ', (MIB('192.168.0.16').cpu_statistics))
    print('CPU Times: ', MIB('192.168.0.16').cpu_times)
    print('System info: ', MIB('192.168.0.16').system_info)

class MemoryStatistics:

    TOTAL_SWAP_SIZE_OID = '.1.3.6.1.4.1.2021.4.3.0'
    AVAILABLE_SWAP_SPACE__OID = '.1.3.6.1.4.1.2021.4.4.0'

    TOTAL_RAM_IN_MACHINE_OID = '.1.3.6.1.4.1.2021.4.5.0'
    TOTAL_RAM_USED_OID = '.1.3.6.1.4.1.2021.4.6.0'
    TOTAL_RAM_FREE_OID = '.1.3.6.1.4.1.2021.4.11.0'
    TOTAL_RAM_SHARED_OID = '.1.3.6.1.4.1.2021.4.13.0'
    TOTAL_RAM_BUFFERED_OID = '.1.3.6.1.4.1.2021.4.14.0'

    TOTAL_CACHED_MEMORY = '.1.3.6.1.4.1.2021.4.15.0'

    @classmethod
    def total_swap_size(cls):
        """
        Tamanho total de swap
        :return: .1.3.6.1.4.1.2021.4.3.0
        """
        return cls.TOTAL_SWAP_SIZE_OID

    @classmethod
    def available_swap_space(cls):
        """
        Espaço de troca disponível
        :return: .1.3.6.1.4.1.2021.4.4.0
        """
        return cls.AVAILABLE_SWAP_SPACE__OID

    @classmethod
    def total_ram_in_machine(cls):
        """
        RAM total na máquina
        :return: .1.3.6.1.4.1.2021.4.5.0
        """
        return cls.TOTAL_RAM_IN_MACHINE_OID

    @classmethod
    def total_ram_used(cls):
        """
        RAM total usada
        :return: .1.3.6.1.4.1.2021.4.6.0
        """
        return cls.TOTAL_RAM_USED_OID

    @classmethod
    def total_ram_free(cls):
        """
        RAM Total Livre
        :return: .1.3.6.1.4.1.2021.4.11.0
        """
        return cls.TOTAL_RAM_FREE_OID

    @classmethod
    def total_ram_shared(cls):
        """
        RAM total compartilhada
        :return: .1.3.6.1.4.1.2021.4.13.0
        """
        return cls.TOTAL_RAM_SHARED_OID

    @classmethod
    def total_ram_buffered(cls):
        """
        RAM total em buffer
        :return: .1.3.6.1.4.1.2021.4.14.0
        """
        return cls.TOTAL_RAM_BUFFERED_OID

    @classmethod
    def total_cached_memory(cls):
        """
        Memória Total em Cache
        :return: .1.3.6.1.4.1.2021.4.15.0
        """
        return cls.TOTAL_CACHED_MEMORY


class DiskStatistics:

    PATH_WHERE_THE_DISK_IS_MOUNTED_OID = '.1.3.6.1.4.1.2021.9.1.2'
    PATH_OF_THE_DEVICE_FOR_THE_PARTITION_OID = '.1.3.6.1.4.1.2021.9.1.3'
    TOTAL_SIZE_OF_THE_DISK_OR_PARTITION_OID = '.1.3.6.1.4.1.2021.9.1.6'
    AVAILABLE_SPACE_ON_THE_DISK_OID = '.1.3.6.1.4.1.2021.9.1.7'
    USED_SPACE_ON_THE_DISK_OID = '.1.3.6.1.4.1.2021.9.1.8'
    PERCENTAGE_OF_SPACE_USED_ON_DISK_OID = '.1.3.6.1.4.1.2021.9.1.9'
    PERCENTAGE_OF_INODES_USED_ON_DISK_OID = '.1.3.6.1.4.1.2021.9.1.10'

    DISK_STORAGE_CAPACITY = '1.3.6.1.2.1.25.3.6'

    @classmethod
    def path_where_the_disk_is_mounted(cls):
        return cls.PATH_WHERE_THE_DISK_IS_MOUNTED_OID

    @classmethod
    def path_of_the_device_for_the_partition(cls):
        return cls.PATH_OF_THE_DEVICE_FOR_THE_PARTITION_OID

    @classmethod
    def total_size_of_disk_or_partition(cls):
        return cls.TOTAL_SIZE_OF_THE_DISK_OR_PARTITION_OID

    @classmethod
    def available_space_on_the_disk(cls):
        return cls.AVAILABLE_SPACE_ON_THE_DISK_OID

    @classmethod
    def used_space_on_the_disk(cls):
        return cls.USED_SPACE_ON_THE_DISK_OID

    @classmethod
    def percentage_of_space_used_on_disk(cls):
        return cls.PERCENTAGE_OF_SPACE_USED_ON_DISK_OID

    @classmethod
    def percentage_of_inodes_used_on_disk(cls):
        return cls.PERCENTAGE_OF_INODES_USED_ON_DISK_OID

    @classmethod
    def disk_storage_capacity(cls):
        return  cls.DISK_STORAGE_CAPACITY

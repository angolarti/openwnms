class System:

    SYSTEM_UPTIME_OID = '.1.3.6.1.2.1.1.3.0'
    TOTAL_SYSTEM_PROCESSES_OID = '.1.3.6.1.2.1.25.1.6'
    AMOUNT_TIME_HOST_WAS_LAST_INITIALIZED_OID = '.1.3.6.1.2.1.25.1.1'
    SYSTEM_DESCRIPTION_OID = '.1.3.6.1.2.1.1.1.0'
    HOSTNAME_OID = '.1.3.6.1.2.1.1.5.0'
    SYSTEM_LOCATION_OID = '.1.3.6.1.2.1.1.6'
    SYSTEM_CONTACT = '.1.3.6.1.2.1.1.4.0'


    @classmethod
    def system_uptime(cls):
        """
        Tempo de actividade do sistema
        :return: .1.3.6.1.2.1.1.3.0
        """
        return cls.SYSTEM_UPTIME_OID

    @classmethod
    def amount_time_host_was_last_initialized(cls):
        return cls.AMOUNT_TIME_HOST_WAS_LAST_INITIALIZED_OID

    @classmethod
    def get_software_installed(cls):
        return '.1.3.6.1.2.1.25.4'

    @classmethod
    def total_processes(cls):
        """
        :return: .1.3.6.1.2.1.25.1.6
        """
        return cls.TOTAL_SYSTEM_PROCESSES_OID

    @classmethod
    def system_description(cls):
        """
        :return:  .1.3.6.1.2.1.1.1.0
        """
        return cls.SYSTEM_DESCRIPTION_OID

    @classmethod
    def get_hostname(cls):
        return cls.HOSTNAME_OID

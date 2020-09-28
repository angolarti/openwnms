class CPUStatistic:

    ONE_MINUTE_LOAD_OID = '.1.3.6.1.4.1.2021.10.1.3.1'
    FIVE_MINUTE_LOAD_OID = '.1.3.6.1.4.1.2021.10.1.3.2'
    FIFTEEN_MINUTE_LOAD_OID = '.1.3.6.1.4.1.2021.10.1.3.3'

    @classmethod
    def one_minute_load(cls):
        """
        one minuto de carga
        :return: .1.3.6.1.4.1.2021.10.1.3.1
        """
        return cls.ONE_MINUTE_LOAD_OID

    @classmethod
    def five_minute_load(cls):
        """
        cinco minutos de carga
        :return: .1.3.6.1.4.1.2021.10.1.3.2
        """
        return cls.FIVE_MINUTE_LOAD_OID

    @classmethod
    def fifteen_minute_load(cls):
        """
        quinze minutos de carga
        :return: .1.3.6.1.4.1.2021.10.1.3.3
        """
        return cls.FIFTEEN_MINUTE_LOAD_OID


class CPUTimes:

    PERCENTAGE_OF_USER_CPU_TIME_OID = '.1.3.6.1.4.1.2021.11.9.0'
    RAW_USER_CPU_TIME_OID = '.1.3.6.1.4.1.2021.11.50.0'
    PERCENTAGES_OF_SYSTEM_CPU_TIME_OID = '.1.3.6.1.4.1.2021.11.10.0'
    RAW_SYSTEM_CPU_TIME_OID = '.1.3.6.1.4.1.2021.11.52.0'
    PERCENTAGES_OF_IDLE_CPU_TIME_OID = '.1.3.6.1.4.1.2021.11.11.0'
    RAW_IDLE_CPU_TIME_OID = '.1.3.6.1.4.1.2021.11.53.0'
    RAW_NICE_CPU_TIME_OID = '.1.3.6.1.4.1.2021.11.51.0'

    @classmethod
    def percentage_of_user_cpu_time(cls):
        """
        porcentagem de tempo de CPU do utilizador
        :return: .1.3.6.1.4.1.2021.11.9.0
        """
        return cls.PERCENTAGE_OF_USER_CPU_TIME_OID

    @classmethod
    def raw_user_cpu_time(cls):
        """
        tempo bruto de CPU do utilizador
        :return: .1.3.6.1.4.1.2021.11.50.0
        """
        return cls.RAW_USER_CPU_TIME_OID

    @classmethod
    def percentages_of_system_cpu_time(cls):
        """
        percentagens de tempo de CPU do sistema
        :return: .1.3.6.1.4.1.2021.11.10.0
        """
        return cls.PERCENTAGES_OF_SYSTEM_CPU_TIME_OID

    @classmethod
    def raw_system_cpu_time(cls):
        """
        tempo de CPU do sistema bruto
        :return: 1.3.6.1.4.1.2021.11.52.0
        """
        return cls.RAW_SYSTEM_CPU_TIME_OID

    @classmethod
    def percentages_of_idle_cpu_time(cls):
        """
        percentagens de tempo de CPU ocioso
        :return: .1.3.6.1.4.1.2021.11.11.0
        """
        return cls.PERCENTAGES_OF_IDLE_CPU_TIME_OID

    @classmethod
    def raw_idle_cpu_time(cls):
        """
        tempo bruto de cpu inativo
        :return: .1.3.6.1.4.1.2021.11.53.0
        """
        return cls.RAW_IDLE_CPU_TIME_OID

    @classmethod
    def raw_nice_cpu_time(cls):
        """
        bom tempo de CPU
        :return: .1.3.6.1.4.1.2021.11.51.0
        """
        return cls.RAW_NICE_CPU_TIME_OID

class System:

    SYSTEM_UPTIME = '.1.3.6.1.2.1.1.3.0'

    @classmethod
    def system_uptime(cls):
        """
        Tempo de actividade do sistema
        :return: .1.3.6.1.2.1.1.3.0
        """
        return cls.SYSTEM_UPTIME

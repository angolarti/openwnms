class NetworkInterfaceStatistics:

    LIST_NIC_NAMES = '.1.3.6.1.2.1.2.2.1.2'
    GET_BYTES_IN = '.1.3.6.1.2.1.2.2.1.10'
    GET_BYTES_IN_FOR_NIC_FOUR = '.1.3.6.1.2.1.2.2.1.10.4'
    GET_BYTES_OUT = '.1.3.6.1.2.1.2.2.1.16'
    GET_BYTES_OUT_FOR_NIC_FOUR = '.1.3.6.1.2.1.2.2.1.16.4'

    @classmethod
    def list_nic_names(cls):
        """
        Listar nomes de NIC
        :return: .1.3.6.1.2.1.2.2.1.2
        """
        return cls.LIST_NIC_NAMES

    @classmethod
    def get_bytes_in(cls):
        """
        Obter bytes de entrada
        :return: .1.3.6.1.2.1.2.2.1.10
        """
        return cls.GET_BYTES_IN

    @classmethod
    def get_bytes_out(cls):
        """
        Obter bytes de saida
        :return: .1.3.6.1.2.1.2.2.1.16
        """
        return cls.GET_BYTES_OUT

    @classmethod
    def get_bytes_in_for_nic_four(cls):
        """
        Obtenha Bytes de ntrada para NIC 4
        :return: .1.3.6.1.2.1.2.2.1.10.4
        """
        return cls.GET_BYTES_IN_FOR_NIC_FOUR

    @classmethod
    def get_bytes_in_for_nic_four(cls):
        """
        Obtenha Bytes de ntrada para NIC 4
        :return: .1.3.6.1.2.1.2.2.1.16.4
        """
        return cls.GET_BYTES_IN_FOR_NIC_FOUR

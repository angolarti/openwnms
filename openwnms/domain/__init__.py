def collection(cls):

    def model_to_collection(self):
        fields = dict((attr, value) for attr, value in cls.__dict__.items() if attr[:2] != '__')
        fields.update(self.__dict__)

        for attr, value in fields.items():
            yield attr, value

    cls.__dict__ = model_to_collection

    return cls

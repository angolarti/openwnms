import types


def collection(cls, **kwargs):

    if 'name' in kwargs.keys():
        pass

    def model_to_collection(self):
        fields = dict((attr, value) for attr, value in cls.__dict__.items()
                      if attr[:2] != '__' and isinstance(attr, types.FunctionType))
        fields.update(self.__dict__)

        for attr, value in fields.items():
            yield attr, value

    cls.__iter__ = model_to_collection
    return cls


class Collection:

    def __dict__(self):
        pass

    def __iter__(self):
        pass

    def __len__(self):
        pass

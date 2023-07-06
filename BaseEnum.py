from enum import Enum, EnumMeta, auto

class MetaEnum(EnumMeta):
    def __contains__(cls, item):
        try:
            cls(item)
        except ValueError:
            return False
        return True    

class BaseEnum(Enum, metaclass=MetaEnum):
    pass

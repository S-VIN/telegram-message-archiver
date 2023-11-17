import os

class EnumToIntConverter:
    _enum_pairs_ = list()

    def __int__(self, input_enum):
        self._enum_pairs_ = __dict__['_member_names_']

    @classmethod
    def enum_to_int(cls, input_enum_string):
        if input_enum_string not in cls._enum_pairs_:
            cls._enum_pairs_.append(input_enum_string)
        return cls._enum_pairs_.index(input_enum_string)




class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class FileSystem:
    @staticmethod
    def is_file_in_filesystem(filename_without_extention, filepath):
        file_list = os.listdir(filepath)
        for i in range(len(file_list)):
            file_list[i] = file_list[i].split('.')[0]

        return filename_without_extention in file_list

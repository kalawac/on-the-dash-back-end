from enum import Enum

class Gender(int, Enum):
    FEMALE = 1
    MALE = 2
    NONBINARY = 3
    OTHER = 4
    UNKNOWN = 9
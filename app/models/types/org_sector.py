from enum import Enum

class OrgSector(int, Enum):
    ACADEMIA = 1
    NGO = 2
    GOVT = 3
    MEDIA = 4
    BUSINESS = 5
    CSR = 6
    SOC_ENT = 7
    IDP = 8
    OTHER = 99
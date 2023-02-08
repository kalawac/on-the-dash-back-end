from enum import Enum

class Subject(int, Enum):
    ACCOUNTING = 1
    ANTI_CORR_GEN = 2
    ANTI_CORR_FOR_ACC = 3
    ANTI_CORR_MON_GOV = 4
    ANTI_CORR_MON_STA = 5
    ANTI_CORR_PROCURE = 6
    CIV_ED = 7
    CONFLICT_MED = 8
    CONFLICT_RES = 9
    CONSENSUS_BUILD = 10
    OTHER = 99
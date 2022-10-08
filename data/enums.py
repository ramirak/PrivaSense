from enum import Enum


class erase_algorithms(Enum):
   DOD_5220_22_m = 1
   HMG_IS5 = 2
   ISM_6_2_92 = 3
   RCMP_TSSIT_OPS_II = 4


class enc_algorithms(Enum):
   AES_256_CFB = 1


class results(Enum):
   ERR_UNKNOWN = 0
   ERR_NOT_ENCRYPTED = 1
   ERR_DIFFERENT_METHOD = 2
   ERR_ALREADY_ENCRYPTED = 3 
   ERR_INVALID_KEY = 4
   SUCCESS = 5
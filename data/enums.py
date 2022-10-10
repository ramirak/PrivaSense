from enum import Enum
from tkinter import messagebox

class erase_algorithms(Enum):
   DOD_5220_22_m = 1
   HMG_IS5 = 2
   ISM_6_2_92 = 3
   RCMP_TSSIT_OPS_II = 4


class enc_algorithms(Enum):
   AES_256_CFB = 1


class filtering(Enum):
   DEFAULT = 1
   ADAWAY = 2
   MICROSOFT = 3
   ULTIMATE = 4


class results(Enum):
   ERR_UNKNOWN = 0
   ERR_NOT_ENCRYPTED = 1
   ERR_DIFFERENT_METHOD = 2
   ERR_ALREADY_ENCRYPTED = 3 
   ERR_INVALID_KEY = 4
   ALREADY_RUNNING = 5
   MULTIPLE_ERRORS = 6
   PARTLY_SUCCESS = 7
   SUCCESS = 8


class dns(Enum):
   DEFAULT_DHCP = 1
   CLOUDFLARE = 2
   OPEN_DNS = 3
   DNS_WATCH = 4
   QUAD9 = 5


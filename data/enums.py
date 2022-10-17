from enum import Enum
from tkinter import messagebox
import winreg

class erase_algorithms(Enum):
   DOD_5220_22_m = 1
   HMG_IS5 = 2
   ISM_6_2_92 = 3
   RCMP_TSSIT_OPS_II = 4


class enc_algorithms(Enum):
   AES_256_CFB = 1


class generators(Enum):
   SECURE_PASSWORD = 1
   SSH_KEY = 2
   FAKE_FORM = 3


class filtering(Enum):
   DEFAULT = 1
   ADAWAY = 2
   MICROSOFT = 3
   ULTIMATE = 4
   CRAZY_MAX = 5

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
   DEFAULT_DHCP = None
   CLOUDFLARE = ["1.1.1.1", "1.0.0.1"]
   OPEN_DNS = ["208.67.222.123", "208.67.220.123"]
   DNS_WATCH = ["84.200.69.80", "84.200.70.40"]
   QUAD9 = ["9.9.9.9", "149.112.112.112"]


class paths(Enum):
   RECYCLE = "systemdrive%\\$Recycle.Bin"
   TEMP = "systemdrive%\\Windows\\Temp",
   WER = "systemdrive%\\ProgramData\\Microsoft\\Windows\\WER\\ReportArchive",
   DOWNLOADS = "userprofile%\\Downloads",
   RECENTS = "userprofile%\\AppData\\Roaming\\Microsoft\\Windows\\Recent",
   OFFICE = "userprofile%\\AppData\\Roaming\\Microsoft\\Office\\Recent",
   EXPLORER_THUMB = "localappdata%\\Microsoft\\Windows\\Explorer",
   SESSIONS = "localappdata%\\Microsoft\\Edge\\User Data\\Default\\Sessions",
   LOCAL_TEMP = "localappdata%\\Temp"

import ctypes, sys, os
from genericpath import isfile
import data.enums as enums
import os_priv.blacklist as blacklist

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def run_as_admin():
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        exit(0)


def reset_changes():
    if os.path.isfile("garbage"):
        os.remove("garbage")
    ## Default host file
    blacklist.replace_host_file(False, enums.filtering.DEFAULT.name)
    ## Dns via DHCP
    blacklist.change_dns(enums.filtering.DEFAULT.name)
    ## Reset the network stack in case of problems
    net_cmd = ["ipconfig /release", "ipconfig /flushdns", "netsh int ip reset", "netsh winsock reset", "ipconfig /release"]
    for cmd in net_cmd:
        os.system(cmd)
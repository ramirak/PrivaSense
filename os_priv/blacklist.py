from fileinput import filename
from .os_utils import *
import os 
import shutil

custom_hosts_path = "hosts"

def replace_host_file(hostfile_name, backup_flag):
    if not is_admin():
        run_as_admin()
    host_path = os.environ["systemdrive"] + "\\Windows\\System32\\Drivers\\etc\\hosts"
    try:
        ## Only backup if flag is true and if not backed up already
        if(backup_flag and not os.path.isfile(custom_hosts_path + "/hosts")):    
            shutil.copy(host_path, custom_hosts_path)

        with open(custom_hosts_path + "/" + hostfile_name, "r") as custom_hosts:
            hosts = custom_hosts.read()
            with open(host_path, "w") as system_hosts:
                system_hosts.write(hosts)
        return 1
    except:
        return 0


def reset_hosts_file():
    try:
        replace_host_file("hosts", False)
        return 1
    except:
        return 0

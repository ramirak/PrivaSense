from .os_utils import *
import os, psutil, shutil
import data.enums as enums


custom_hosts_path = "hosts"

def replace_host_file(backup_flag, hostfile_name):
    host_path = os.environ["systemdrive"] + "\\Windows\\System32\\Drivers\\etc\\hosts"
    try:
        ## Only backup if flag is true and if not backed up already
        if(backup_flag and not os.path.isfile(custom_hosts_path + "/hosts")):    
            shutil.copy(host_path, custom_hosts_path)

        with open(custom_hosts_path + "/" + hostfile_name, "r") as custom_hosts:
            hosts = custom_hosts.read()
            with open(host_path, "w") as system_hosts:
                system_hosts.write(hosts)
        return enums.results.SUCCESS.value
    except:
        return enums.results.ERR_UNKNOWN.value


def reset_hosts_file():
    try:
        replace_host_file("hosts", False)
        return enums.results.SUCCESS.value
    except:
        return enums.results.ERR_UNKNOWN.value


def change_dns(dns_provider):
    addrs = psutil.net_if_addrs()
    provider_ip = []

    if dns_provider == enums.dns.CLOUDFLARE.name:
        provider_ip.append("1.1.1.1")
        provider_ip.append("1.0.0.1")
    elif dns_provider == enums.dns.DNS_WATCH.name:
        provider_ip.append("84.200.69.80")
        provider_ip.append("84.200.70.40")
    elif dns_provider == enums.dns.OPEN_DNS.name:
        provider_ip.append("208.67.222.123")
        provider_ip.append("208.67.220.123")
    elif dns_provider == enums.dns.QUAD9.name:
        provider_ip.append("9.9.9.9")
        provider_ip.append("149.112.112.112")
    elif dns_provider == enums.dns.DEFAULT_DHCP.name:
        for i in addrs:
            cmd = "netsh interface ipv4 set dnsservers \"%s\" dhcp" % (i) 
            os.system(cmd)
        return enums.results.SUCCESS.value
    else:
        return enums.results.ERR_UNKNOWN.value

    for i in addrs:
        dns1 = "netsh interface ipv4 set dnsservers \"%s\" static %s primary" % (i, provider_ip[0]) 
        dns2 = "netsh interface ip add dns name=\"%s\" %s index=2" % (i, provider_ip[1]) 
        os.system(dns1)
        os.system(dns2)        
    return enums.results.SUCCESS.value



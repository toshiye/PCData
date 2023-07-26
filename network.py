import json
import subprocess
import socket
import netifaces
import platform
import os

def get_current_user():
    return os.getlogin()

def get_ip_addresses():
    ip_addresses = []
    for interface in netifaces.interfaces():
        addrs = netifaces.ifaddresses(interface).get(netifaces.AF_INET)
        if addrs:
            for addr_info in addrs:
                ip_addresses.append(addr_info['addr'])
    return ip_addresses

def get_mac_address():
    try:
        mac_address = ':'.join(hex(i)[2:].zfill(2) for i in netifaces.ifaddresses('Ethernet0')[netifaces.AF_LINK][0]['addr'].encode('ascii'))
        return mac_address
    except Exception as e:
        return None

def get_network_mask():
    try:
        return netifaces.ifaddresses('Ethernet0')[netifaces.AF_INET][0]['netmask']
    except Exception as e:
        return None

def get_dns_servers():
    try:
        dns_servers = []
        for addr in socket.getaddrinfo(socket.gethostname(), None):
            if addr[1] == socket.SOCK_STREAM:
                dns_servers.append(addr[4][0])
        return dns_servers
    except Exception as e:
        return None

def get_gateway():
    return netifaces.gateways()['default'][netifaces.AF_INET][0]

def get_ip_domain():
    try:
        return socket.getfqdn()
    except Exception as e:
        return None

def get_last_user_login():
    # You might need platform-specific commands to get this information
    # For example, on Linux, you can use 'last' command to get the last logged-in users.
    # On Windows, you can access event logs.
    return None

def get_working_group_domain():
    return platform.node()

def get_network_type():
    return platform.system()

def is_dhcp_active():
    # You might need to check the DHCP service status on the system
    return False

def get_biggest_user():
    # You'll need to define how you determine the "biggest user" - this could mean highest network usage, most data transferred, etc.
    return None

# Gather network information
network_info = {
    "Current User": get_current_user(),
    "IP Addresses": get_ip_addresses(),
    "MAC Address": get_mac_address(),
    "Network Mask": get_network_mask(),
    "DNS Servers": get_dns_servers(),
    "Gateway": get_gateway(),
    "IP Domain": get_ip_domain(),
    "Last User to Login": get_last_user_login(),
    "Working Group / Domain": get_working_group_domain(),
    "Type": get_network_type(),
    "Active DHCP": is_dhcp_active(),
    "Biggest User": get_biggest_user()
}

# Convert the network_info dictionary to JSON
network_info_json = json.dumps(network_info, indent=4)

# You can send the JSON to a server or save it to a file
# For example, saving to a file named "network_info.json":
with open("network_info.json", "w") as json_file:
    json_file.write(network_info_json)

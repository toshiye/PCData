import platform
import socket
import psutil
import getpass
import json
import requests
from datetime import datetime, timedelta
import subprocess
import winreg
import pytz

# Retrieve the hostname
hostname = socket.gethostname()

# Retrieve the IP address
ip_address = socket.gethostbyname(hostname)

# Retrieve the operating system name
operating_system = platform.system()

# Retrieve the CPU details
cpu_info = platform.processor()

# Retrieve the memory (RAM) details
memory_info = psutil.virtual_memory()

# Retrieve the disk usage details
disk_info = psutil.disk_usage('/')

# Retrieve the network interfaces and their addresses
network_interfaces = psutil.net_if_addrs()

# Retrieve the logged-in username
username = getpass.getuser()

# Retrieve the current hour
current_hour = datetime.now().strftime("%H:%M:%S")

# Retrieve location based on IP address
response = requests.get(f"http://ip-api.com/json/{ip_address}")
location_data = response.json()

# Retrieve the date of activation
activation_date = None
if operating_system == "Windows":
    cmd_output = subprocess.check_output(["wmic", "os", "get", "installdate", "/value"]).decode("utf-8").strip()
    if cmd_output.startswith("InstallDate="):
        install_date_str = cmd_output[len("InstallDate="):]
        if len(install_date_str) >= 8:
            activation_date = datetime.strptime(install_date_str, "%Y%m%d").date()

# Convert activation date to Brazilian time
if activation_date:
    brazil_tz = pytz.timezone('America/Sao_Paulo')
    activation_date = datetime.combine(activation_date, datetime.min.time())
    activation_date = pytz.utc.localize(activation_date).astimezone(brazil_tz)

# Retrieve the installed software based on key registry
software_list = []
uninstall_key = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
root_key = winreg.HKEY_LOCAL_MACHINE
try:
    with winreg.OpenKey(root_key, uninstall_key) as key:
        num_subkeys = winreg.QueryInfoKey(key)[0]
        for i in range(num_subkeys):
            subkey_name = winreg.EnumKey(key, i)
            subkey_path = f"{uninstall_key}\\{subkey_name}"
            with winreg.OpenKey(root_key, subkey_path) as subkey:
                try:
                    display_name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                    software_list.append(display_name)
                except OSError:
                    continue
except FileNotFoundError:
    pass

# Create a dictionary with all the information
computer_info = {
    "Hostname": hostname,
    "IP Address": ip_address,
    "Operating System": operating_system,
    "CPU": cpu_info,
    "Memory": {
        "Total": memory_info.total,
        "Available": memory_info.available,
        "Used": memory_info.used,
        "Percentage": memory_info.percent
    },
    "Disk Usage": {
        "Total": disk_info.total,
        "Used": disk_info.used,
        "Free": disk_info.free,
        "Percentage": disk_info.percent
    },
    "Network Interfaces": {
        interface: [address.address for address in addresses]
        for interface, addresses in network_interfaces.items()
    },
    "Logged-in Username": username,
    "Current Hour": current_hour,
    "Location": {
        "IP Address": ip_address,
        "City": location_data.get("city"),
        "Country": location_data.get("country"),
        "Region": location_data.get("regionName"),
        "ZIP Code": location_data.get("zip")
    },
    "Activation Date": activation_date.strftime("%Y-%m-%d %H:%M:%S") if activation_date else None,
    "Installed Software": software_list
}

# Save the information to a JSON file
output_file = "computer_info.json"
with open(output_file, "w") as file:
    json.dump(computer_info, file, indent=4)

print("Computer information saved to", output_file)

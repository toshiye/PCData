import psutil
import platform
import json

def is_notebook():
    # Check if the system has a battery and is a portable/laptop device
    return platform.system() == "Windows" and psutil.sensors_battery() is not None

def get_system_info():
    system_info = {}

    # Last Modified Date (for this script, we'll use the current date)
    system_info["Last Modified Date"] = "2023-07-26"

    # Department and Department with Hierarchy (replace with actual values)
    system_info["Department"] = "Your Department"
    system_info["Department with Hierarchy"] = "Your Department > Subdepartment > Sub-subdepartment"

    # Check if it's a notebook (laptop)
    system_info["It's a notebook"] = is_notebook()

    # Check if it's a virtual machine
    system_info["It's a virtual machine"] = platform.system() == "Linux" and "hypervisor" in platform.uname().release.lower()

    # Operational System, System Type, and Operating System Version
    system_info["Operational system"] = platform.system()
    system_info["System Type"] = platform.machine()
    system_info["Operating system version"] = platform.version()

    # Amount of RAM (MB)
    system_info["Amount of RAM (MB)"] = psutil.virtual_memory().total >> 20  # Convert bytes to megabytes

    # Processor information
    cpufreq = psutil.cpu_freq()
    system_info["Processor"] = platform.processor()
    system_info["Processor speed"] = f"{cpufreq.current:.2f} MHz"
    system_info["Number of processors"] = psutil.cpu_count()

    # Computer Description (replace with actual value if available)
    system_info["Computer Description"] = "Your computer description"

    return system_info

def save_to_json(data):
    with open("system_info.json", "w") as json_file:
        json.dump(data, json_file, indent=4)

if __name__ == "__main__":
    system_info = get_system_info()
    save_to_json(system_info)

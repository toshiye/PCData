import wmi
import json
import re
from datetime import datetime

def format_bios_date(bios_date_str):
    if bios_date_str == "N/A":
        return "N/A"

    date_pattern = r"(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})(?:\.\d+)?([+-]\d{2})(\d{2})"
    match = re.match(date_pattern, bios_date_str)
    if match:
        year, month, day, hour, minute, second, tz_hours, tz_minutes = match.groups()
        tz_offset = f"{tz_hours}:{tz_minutes}"
        date_str = f"{year}-{month}-{day} {hour}:{minute}:{second} {tz_offset}"
        date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S %z")
        return date_obj.strftime("%d/%m/%Y %H:%M:%S")
    else:
        return "N/A"

def get_system_info():
    c = wmi.WMI()
    system_info = {}
    for system in c.Win32_ComputerSystem():
        system_info['System Manufacturer'] = system.Manufacturer or 'N/A'
        system_info['Product Name'] = system.Model or 'N/A'
        
    for bios in c.Win32_BIOS():
        system_info['System Serial Number'] = bios.SerialNumber or 'N/A'
        system_info['BIOS Date'] = format_bios_date(bios.ReleaseDate)
    return system_info

def get_motherboard_info():
    c = wmi.WMI()
    motherboard_info = {}
    for board in c.Win32_BaseBoard():
        motherboard_info['Motherboard Manufacturer'] = board.Manufacturer or 'N/A'
        motherboard_info['Motherboard Name'] = board.Product or 'N/A'
        motherboard_info['Motherboard Serial Number'] = board.SerialNumber or 'N/A'
    return motherboard_info

def get_bios_info():
    c = wmi.WMI()
    bios_info = {}
    for bios in c.Win32_BIOS():
        bios_info['BIOS Manufacturer'] = bios.Manufacturer or 'N/A'
        bios_info['BIOS Date'] = format_bios_date(bios.ReleaseDate)
        bios_info['BIOS Version'] = bios.SMBIOSBIOSVersion or 'N/A'
    return bios_info

def get_cabinet_info():
    c = wmi.WMI()
    cabinet_info = {}
    for enclosure in c.Win32_SystemEnclosure():
        cabinet_info['Cabinet Manufacturer'] = enclosure.Manufacturer or 'N/A'
        cabinet_info['Cabinet Version'] = enclosure.Version or 'N/A'
        cabinet_info['Cabinet Serial Number'] = enclosure.SerialNumber or 'N/A'
    return cabinet_info

def main():
    hardware_info = {
        'System Information': get_system_info(),
        'Motherboard Information': get_motherboard_info(),
        'BIOS Information': get_bios_info(),
        'Cabinet Information': get_cabinet_info()
    }

    # Save the hardware information to a JSON file
    with open('hardware_info.json', 'w') as json_file:
        json.dump(hardware_info, json_file, indent=4)

if __name__ == "__main__":
    main()

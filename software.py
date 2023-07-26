import json
import win32com.client

def get_software_info():
    wmi = win32com.client.GetObject('winmgmts:')
    software_items = wmi.InstancesOf('Win32_Product')

    software_list = []
    for software in software_items:
        software_info = {
            'Software Name': software.Name,
            'Version': software.Version,
            'Software Identifier': software.IdentifyingNumber,
            'Manufacturer': software.Vendor,
            'Group': software.SKUNumber,
            'Category': software.Caption,
            # Add other software information fields here
        }
        software_list.append(software_info)

    return software_list

def save_to_json(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

if __name__ == "__main__":
    software_data = get_software_info()
    save_to_json(software_data, "software_info.json")

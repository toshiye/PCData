import json
import wmi

def get_usb_device_info(device):
    return {
        'vendor_id': device.PNPDeviceID.split('\\')[1],
        'product_id': device.PNPDeviceID.split('\\')[2],
        'manufacturer': device.Manufacturer,
        'product': device.Description,
        'serial_number': device.PNPDeviceID.split('\\')[-1],
    }

def get_usb_devices_info():
    devices_info = []
    c = wmi.WMI()
    usb_devices = c.Win32_USBControllerDevice()
    for usb_device in usb_devices:
        device = usb_device.Dependent
        device_info = get_usb_device_info(device)
        devices_info.append(device_info)
    return devices_info

def save_to_json(data, filename):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)

if __name__ == "__main__":
    usb_devices_info = get_usb_devices_info()
    save_to_json(usb_devices_info, 'usb_devices_info.json')

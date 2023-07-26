import wmi
import json

def get_monitor_info():
    c = wmi.WMI()
    monitor_info = []
    
    for monitor in c.Win32_DesktopMonitor():
        monitor_dict = {
            'Serial number': monitor.DeviceID.strip(),
            'Monitor name': monitor.Caption.strip(),
            'Monitor manufacturer': monitor.PNPDeviceID.split('\\')[1].strip(),
            'Week / Year of manufacture': monitor.InstallDate.strip() if monitor.InstallDate else "N/A",
            'Maximum screen size': f"{monitor.ScreenWidth}x{monitor.ScreenHeight}",
            'Current resolution': f"{monitor.ScreenWidth}x{monitor.ScreenHeight}",
            'Maximum resolution': f"{monitor.MaxHorizontalImageSize}x{monitor.MaxVerticalImageSize}" if hasattr(monitor, 'MaxHorizontalImageSize') and hasattr(monitor, 'MaxVerticalImageSize') else "N/A",
            'Horizontal frequency': monitor.MaxHorizontalImageSize if hasattr(monitor, 'MaxHorizontalImageSize') else "N/A",
            'Vertical frequency': monitor.MaxVerticalImageSize if hasattr(monitor, 'MaxVerticalImageSize') else "N/A",
        }
        monitor_info.append(monitor_dict)
    
    return monitor_info

if __name__ == "__main__":
    monitor_info = get_monitor_info()
    
    with open('monitor_info.json', 'w') as json_file:
        json.dump(monitor_info, json_file, indent=4)

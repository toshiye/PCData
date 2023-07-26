import os
import psutil
import json

def get_system_file_info():
    partitions = psutil.disk_partitions()
    system_info = []

    for partition in partitions:
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            total_capacity_gb = usage.total / (1024 ** 3)
            free_space_gb = usage.free / (1024 ** 3)
            used_space_gb = usage.used / (1024 ** 3)

            system_info.append({
                "Unit": partition.device,
                "Total capacity (GB)": round(total_capacity_gb, 2),
                "Free space on partition (GB)": round(free_space_gb, 2),
                "Total used space (GB)": round(used_space_gb, 2)
            })
        except Exception as e:
            print(f"Error getting information for {partition.mountpoint}: {e}")

    return system_info

def save_to_json(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    system_info = get_system_file_info()
    save_to_json(system_info, "system_file_info.json")
    print("System file information has been saved to 'system_file_info.json'")

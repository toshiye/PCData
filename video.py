import platform
import subprocess
import json

def get_video_adapter_info():
    adapters_info = []
    try:
        if platform.system() == "Windows":
            # Windows-specific command to get video adapter information
            cmd = "wmic path win32_videocontroller get caption, driverversion, adapterram"
            result = subprocess.check_output(cmd, shell=True, universal_newlines=True)
            lines = result.strip().split("\n")[1:]
            for line in lines:
                parts = line.strip().split()
                if len(parts) >= 3:
                    adapter_info = {
                        "name": " ".join(parts[:-2]),
                        "driver": parts[-2],
                        "memory": {
                            "total": parts[-1],
                            "free": "N/A",  # We can't get free memory from this command
                            "used": "N/A"   # We can't get used memory from this command
                        }
                    }
                    adapters_info.append(adapter_info)
        else:
            # Linux/Mac-specific command to get video adapter information
            cmd = "lspci | grep -i vga"
            result = subprocess.check_output(cmd, shell=True, universal_newlines=True)
            lines = result.strip().split("\n")
            for line in lines:
                parts = line.strip().split(":")
                if len(parts) == 2:
                    adapter_info = {
                        "name": parts[1].strip(),
                        "driver": "",  # We can't get driver information from this command
                        "memory": {
                            "total": "N/A",  # We can't get memory information from this command
                            "free": "N/A",
                            "used": "N/A"
                        }
                    }
                    adapters_info.append(adapter_info)
    except Exception as e:
        print(f"Error: {e}")
    
    return adapters_info

def main():
    video_adapter_info = get_video_adapter_info()
    if video_adapter_info:
        json_data = json.dumps(video_adapter_info, indent=4)
        with open("video_adapter_info.json", "w") as json_file:
            json_file.write(json_data)
        print("Video adapter information has been saved to 'video_adapter_info.json'")
    else:
        print("No video adapter information found.")

if __name__ == "__main__":
    main()

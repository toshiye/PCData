import psutil
import json

def get_slot_info():
    slot_info = {}

    # Get the number of total slots and slot type (if available)
    slot_info['total_slots'] = psutil.cpu_count(logical=False)
    slot_info['slot_type'] = "CPU"  # Change this if it's not CPU slots

    # Get the number of free slots
    slot_info['free_slots'] = psutil.cpu_count(logical=False) - psutil.cpu_count(logical=True)

    # Get memory information
    memory = psutil.virtual_memory()
    slot_info['total_memory_slots'] = memory.total
    slot_info['free_memory_slots'] = memory.available
    slot_info['memory'] = memory.total

    # Add a description for the slots (optional)
    slot_info['description'] = "This is a description of the CPU/memory slots."

    return slot_info

def save_to_json(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file)

if __name__ == "__main__":
    slot_info = get_slot_info()
    json_file_path = "slot_info.json"
    save_to_json(slot_info, json_file_path)
    print(f"Slot information saved to '{json_file_path}'.")

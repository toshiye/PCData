import serial
import json

def get_modem_information():
    # Replace 'COM1' with the appropriate serial port for your modem
    with serial.Serial('COM1', 115200, timeout=1) as ser:
        # Here, you can use the necessary AT commands to retrieve modem information
        # Modify these commands according to your modem's specifications
        # Example commands (you may need to adjust them based on your modem):
        ser.write(b'AT+CGMI\r')  # Get Manufacturer Name
        manufacturer_name = ser.readline().decode().strip()

        ser.write(b'AT+CGMM\r')  # Get Model Name
        model_name = ser.readline().decode().strip()

        ser.write(b'AT+CGSN\r')  # Get Serial Number
        serial_number = ser.readline().decode().strip()

        ser.write(b'AT+CGMR\r')  # Get Firmware Version
        firmware_version = ser.readline().decode().strip()

    return {
        "Manufacturer Name": manufacturer_name,
        "Model Name": model_name,
        "Serial Number": serial_number,
        "Firmware Version": firmware_version
    }

def save_to_json(data):
    with open('modem_info.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)

def main():
    # Get modem information (sample data, replace with actual modem data)
    modem_info = {
        "Manufacturer Name": "Manufacturer not found",
        "Model Name": "Model not found",
        "Serial Number": "Serial Number not found",
        "Firmware Version": "Firmware Version not found"
    }

    # Save information to a JSON file
    save_to_json(modem_info)

if __name__ == "__main__":
    main()

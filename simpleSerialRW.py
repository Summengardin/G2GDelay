import serial, serial.tools.list_ports


def find_arduino_on_serial_port() -> serial.Serial:
    devices = serial.tools.list_ports.comports()
    for device in devices:
        if device.manufacturer is not None:
            if "Arduino" in device.manufacturer:
                print(f"Found Arduino at {device[0]}")
                return serial.Serial(device[0], 115200, timeout=5)

    raise ConnectionRefusedError("Did not find Arduino on any serial port. Is it connected?")

# Establish serial connection
arduino = find_arduino_on_serial_port()

while True:
    # Send data to Arduino
    message = input("Enter a message to send to Arduino: ")
    arduino.write(message.encode())  # Convert string to bytes and send

    # Read data from Arduino
    response = arduino.readline().decode().rstrip('\r\n')
    print("Response from Arduino:", response)

# Close the serial connection (optional)
arduino.close()
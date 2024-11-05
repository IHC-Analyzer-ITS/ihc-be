import serial

class SerialController:
    def __init__(self, port, baudrate=9600, timeout=1):
        self.ser = None
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout

    def connect(self):
        """Connect to the serial port."""
        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
            return "CONNECTED"
        except serial.SerialException:
            self.ser = None
            return "Unable to connect"

    def send_command(self, command):
        """Send a command to the serial port."""
        if self.ser and self.ser.is_open:
            self.ser.write(command.encode())
            print(f"{command} command sent")
        else:
            print("Error: Not connected to any COM port")

    def up(self):
        """Send the 'up' command."""
        self.send_command('S')

    def down(self):
        """Send the 'down' command."""
        self.send_command('W')

    def left(self):
        """Send the 'left' command."""
        self.send_command('A')

    def right(self):
        """Send the 'right' command."""
        self.send_command('D')

    def disconnect(self):
        """Disconnect from the serial port."""
        if self.ser and self.ser.is_open:
            self.ser.close()
            print("Disconnected from serial port")
        else:
            print("No connection to close")

# Example usage:
# controller = SerialController('COM3')  # Replace 'COM3' with your port
# print(controller.connect())
# controller.up()
# controller.disconnect()

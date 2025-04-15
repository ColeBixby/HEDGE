import utime
import _thread
from machine import Pin,UART
from machine import I2C
from ads1x15 import ADS1115
from max6675 import MAX6675

class RockBlockInterface:
    def __init__(self, tx_pin=8, rx_pin=9, baudrate=19200): #rockblock default
        self.uart = UART(1, baudrate=baudrate, tx=Pin(tx_pin), rx=Pin(rx_pin), timeout=10000)
        utime.sleep(1) #delay for stabilization
        #change UART2 to whatever port the rockblock is connected to on the pico

    def send_command(self, cmd, delay=1):
        self.uart.write((cmd + '\r').encode())
        utime.sleep(delay)
        response = self.uart.read()
        return response.decode() if response else ''

    def send_message(self, message):
        # Ensure modem is responsive
        if 'OK' not in self.send_command('AT'):
            print("RockBlock not responding")
            return False

        self.send_command('AT+SBDWT=' + message)       # Write message to buffer
        result = self.send_command('AT+SBDIX', 10)      # Initiate message transfer
        print("SBDIX Result:", result)
        return "SBDIX" in result


def send_data(data):
    try:
        rockblock = RockBlockInterface()
    except Exception as e:
        print("ERROR CREATING RockBlockInterface", e)
    try:
        # Build a message from all new entries
        # Format: T:23.45@12,T:24.12@13,...
        try:
            message_parts = [
                f"T:{data[1]:.2f}@{data[0]}"
            ]
            message = ','.join(message_parts)
        except Exception as e:
            print("ERROR BUILDING MESSAGE", e)

        # Iridium messages are limited (340 bytes max); truncate if needed
        if len(message) > 340:
            print("Message too long, truncating")
            message = message[:340]

        success = rockblock.send_message(message)
        print("Data sent:", message, "Success:", success)

    except Exception as e:
        print("Error sending data:", e)
from machine import UART, Pin
import utime

# Enable RockBLOCK (GP3 high)
rb_enable = Pin(3, Pin.OUT)
rb_enable.value(1)
utime.sleep(1)

# UART0: TX = GP0, RX = GP1
uart = UART(0, baudrate=19200, tx=Pin(0), rx=Pin(1))

# Check rockblock status
uart.write(b"AT\r")
utime.sleep(1)
response = uart.read()
print("Response:", response)

# Check signal strength
for i in range(40):
    uart.write(b"AT+CSQ\r")
    utime.sleep(2)
    resp = uart.read()
    print(f"Attempt {i+1}: {resp}")
    utime.sleep(5)
from machine import UART, Pin
import utime
import _thread
StopThreads = False
uart = None

def getThreadStatus(status):
    global StopThreads
    StopThreads = status

def initializeTransmission():
    # Step 1: Power on RockBLOCK (GP3 HIGH)
    global uart
    rb_enable = Pin(3, Pin.OUT)
    rb_enable.value(1)
    utime.sleep(2)
    uart = UART(0, baudrate=19200, tx=Pin(0), rx=Pin(1))

# Iridium send function
def send_iridium_message(message):
    def send_cmd(cmd, delay=2):
        uart.write((cmd + '\r').encode())
        utime.sleep(delay)
        resp = uart.read()
        return resp.decode() if resp else ""

    print("Checking RockBLOCK...")
    if "OK" not in send_cmd("AT"):
        print("Modem not responding")
        return False

    print("Writing message to buffer...")
    if "OK" not in send_cmd(f"AT+SBDWT={message}"):
        print("Failed to write message")
        return False

    print("Initiating satellite transfer (SBDIX)...")
    response = send_cmd("AT+SBDIX", delay=10)
    print("SBDIX response:")
    print(response)

    return "+SBDIX:" in response

# Function to send message every 45 seconds
def iridium_loop(compressedData):
    send_count = 1
    print(f"\nSending message #{compressedData}")
    success = send_iridium_message(compressedData)

    if success:
        print(f"Message #{send_count} sent: {compressedData}")
    else:
        print(f"Failed to send message #{send_count}")

    send_count += 1
    utime.sleep(60)

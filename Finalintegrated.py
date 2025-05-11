from machine import UART, Pin
import utime
import urandom
import _thread

# Step 1: Power on RockBLOCK 
rb_enable = Pin(3, Pin.OUT)
rb_enable.value(1)
utime.sleep(2)

# Step 2: UART Setup 
uart = UART(0, baudrate=19200, tx=Pin(0), rx=Pin(1))

# Thread-safe queue for data sets 
data_queue = []
queue_lock = _thread.allocate_lock()

# Helper: AT command sender
def send_cmd(cmd, delay=2):
    uart.write((cmd + '\r').encode())
    utime.sleep(delay)
    timeout = utime.ticks_ms() + 5000
    response = b""
    while utime.ticks_ms() < timeout:
        chunk = uart.read()
        if chunk:
            response += chunk
        else:
            utime.sleep_ms(100)
    return response.decode('utf-8', 'ignore')

# Generate 1 data set in the format: tttTTTTTTTTPPPPPPhv 
def generate_data_set(timestamp):
    t = f"{timestamp % 1000:03}"
    temps = ''.join([f"{10 + urandom.getrandbits(7) % 84:02}" for _ in range(4)])
    pressures = ''.join([f"{100 + urandom.getrandbits(10) % 900:03}" for _ in range(2)])
    h = f"{100 + urandom.getrandbits(10) % 900:03}"
    v = f"{10 + urandom.getrandbits(7) % 90:02}"
    return (t + temps + pressures + h + v).encode('ascii')  # 22 bytes

# === Binary message send function ===
def send_binary_payload(payload):
    print("Starting AT+SBDWB binary write...")

    if len(payload) != 330:
        print(f"Payload is {len(payload)} bytes, not 330.")
        return False

    resp = send_cmd("AT+SBDWB=330", delay=1)
    if "READY" not in resp:
        print("Modem not ready for binary write.")
        return False

    checksum = sum(payload) & 0xFFFF
    uart.write(payload)
    uart.write(bytes([(checksum >> 8) & 0xFF, checksum & 0xFF]))
    utime.sleep(3)

    resp = uart.read()
    if resp and b"0" in resp:
        print("Payload written to buffer.")
    else:
        print("Failed to write payload. Response:", resp)
        return False

    print("Sending with AT+SBDIX...")
    resp = send_cmd("AT+SBDIX", delay=10)
    print("SBDIX response:", resp)

    if "+SBDIX:" in resp:
        try:
            mo_status = int(resp.split("+SBDIX:")[1].split(",")[0].strip())
            if mo_status in [0, 1]:
                print("Message sent successfully!")
                return True
            else:
                print(f"Message failed. MO status = {mo_status}")
        except Exception as e:
            print("Parsing error:", str(e))
    else:
        print("No +SBDIX response")
    return False

# Background data generator 
def data_generator():
    timestamp = 0
    while True:
        dataset = generate_data_set(timestamp)
        with queue_lock:
            data_queue.append(dataset)
        timestamp += 1
        utime.sleep(1)

# Sender: runs for 348 seconds, sends every 15 seconds 
def timed_iridium_sender(duration_sec=348, interval_sec=15):
    start_time = utime.time()
    while utime.time() - start_time < duration_sec:
        with queue_lock:
            if len(data_queue) >= 15:
                batch = b''.join(data_queue[:15])  # 15 sets × 22 bytes = 330 bytes
                print(f"Attempting transmission at {utime.time() - start_time:.0f}s...")
                success = send_binary_payload(batch)
                if success:
                    del data_queue[:15]
        utime.sleep(interval_sec)
    print("Completed all transmissions in 348 seconds.")

#  Start threads 
_thread.start_new_thread(data_generator, ())
timed_iridium_sender(duration_sec=348, interval_sec=15)

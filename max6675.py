import time
from machine import Pin

class MAX6675:
    MEAS_MS = 220

    def __init__(self, sck_pin=18, cs_pin=23, so_pin=19):
        sck = Pin(sck_pin, Pin.OUT)
        cs = Pin(cs_pin, Pin.OUT)
        so = Pin(so_pin, Pin.IN)

        self._sck = sck
        self._sck.value(0)

        self._cs = cs
        self._cs.value(1)

        self._so = so
        self._so.value(0)

        self._last_meas_start = 0
        self._last_read_temp = 0
        self._error = 0

    def _cycle_sck(self):
        self._sck.value(1)
        time.sleep_us(1)
        self._sck.value(0)
        time.sleep_us(1)

    def refresh(self):
        """
        Start a new measurement.
        """
        self._cs.value(0)
        time.sleep_us(10)
        self._cs.value(1)
        self._last_meas_start = time.ticks_ms()

    def ready(self):
        """
        Signals if measurement is finished.
        :return: True if measurement is ready for reading.
        """
        elapsed = time.ticks_ms() - self._last_meas_start
        return elapsed > MAX6675.MEAS_MS

    def error(self):
        """
        Returns error bit of last reading.
		If this bit is set (=1), there's problem with the
        thermocouple - it can be damaged or loosely connected
        :return: Error bit value
        """
        return self._error

    def read(self):
        """
        Reads last measurement and starts a new one.
		If new measurement is not ready yet, returns last value.
        Note: The last measurement can be quite old
        To refresh measurement, call refresh and wait for
		  ready to become True before reading.
        :return: Measured temperature
        """
        # Check if new reading is available
        if self.ready():
            # Bring CS pin low to start protocol for reading result of
            # the conversion process. Forcing the pin down outputs
            # first (dummy) sign bit 15.
            self._cs.value(0)
            time.sleep_us(10)

            # Read temperature bits 14-3 from MAX6675.
            value = 0
            for i in range(12):
                # SCK should resemble clock signal and new SO value
                # is presented at falling edge
                self._cycle_sck()
                value += self._so.value() << (11 - i)

            # Read the TC Input pin to check if the input is open
            self._cycle_sck()
            self._error = self._so.value()

            # Read the last two bits to complete protocol
            for i in range(2):
                self._cycle_sck()

            # Finish protocol and start new measurement
            self._cs.value(1)
            self._last_meas_start = time.ticks_ms()

            self._last_read_temp = value * 0.25

        return self._last_read_temp

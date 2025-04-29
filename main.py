import utime, _thread
import IridiumTransmission as Transmitter
from machine import Pin, UART, I2C
from ads1x15 import ADS1115, ADS1015
from max6675 import MAX6675
StopThread = False
Transmitter.initializeTransmission()

class DataHandling:
    def add_entry(self, dataframe, values):
        dataframe.append(values)
        return dataframe

    def get_send_indicator(self):
        return True

    def clear_dataframes(self, temp, press, gnss):
        if self.get_send_indicator():
            temp.clear()
            press.clear()
            gnss.clear()

    def initializeThermocouples(self):
        i2c = I2C(0, sda=Pin(12), scl=Pin(13), freq=400_000)
        self.tempSensor1 = ADS1015(i2c, address=0x4A, gain=5)

    def collect_temp(self):
        try:
            current_time = utime.localtime()[5]
            raw = self.tempSensor1.read(rate=0, channel1=0)  
            volts = self.tempSensor1.raw_to_v(raw)
            temperature_c = volts / 0.000041
            return (current_time, temperature_c)
        except Exception as e:
            print("ERROR IN collect_temp", e)
            return None

    def collect_press(self):
        try:
            i2c = I2C(0, sda=Pin(12), scl=Pin(13))
            ads1 = ADS1115(i2c, address=0x48, gain=0)
            ads2 = ADS1115(i2c, address=0x49, gain=0)

            current_time = utime.localtime()[5]
            value = ads1.read(4, 0)
            press1 = ads1.raw_to_v(value)
            value = ads2.read(4, 0)
            press2 = ads2.raw_to_v(value)

            return (current_time, press1, press2)
        except Exception as e:
            print("ERROR IN collect_press", e)
            return None

    def collect_gnss(self):
        try:
            current_time = utime.localtime()[5]
            gnss = UART(1,baudrate=9600,tx=Pin(4),rx=Pin(5),timeout=2000)
            return (current_time, gnss)
        except Exception as e:
            print("ERROR IN collect_gnss", e)
            return None

    def store_temperature(self, df):
        global StopThread
        while StopThread == False:
            start = utime.ticks_ms()
            temp_data = self.collect_temp()
            if temp_data is not None:
                self.add_entry(df, temp_data)
            elapsed = utime.ticks_diff(utime.ticks_ms(), start)
            if elapsed < 500:
                utime.sleep_ms(500 - elapsed)
            print("Temp 1 Data:")
            print(df)
            # Add iridium transmission code here
            global Transmitter
            Transmitter.iridium_loop(str(df))
            print()

    def store_pressure(self, df):
        global StopThread
        while StopThread == False:
            start = utime.ticks_ms()
            press_data = self.collect_press()
            if press_data is not None:
                self.add_entry(df, press_data)
            elapsed = utime.ticks_diff(utime.ticks_ms(), start)
            if elapsed < 500:
                utime.sleep_ms(500 - elapsed)
            print("Pressure Data:")
            print(df)
            print()

    def store_gnss(self, df):
        global StopThread
        while StopThread == False:
            start = utime.ticks_ms()
            gnss_data = self.collect_gnss()
            if gnss_data is not None:
                self.add_entry(df, gnss_data)
            elapsed = utime.ticks_diff(utime.ticks_ms(), start)
            if elapsed < 500:
                utime.sleep_ms(500 - elapsed)
            print("GNSS Data:")
            print(df)
            print()

def build_dataframes():
    dh = DataHandling()
    dh.initializeThermocouples()

    try:
        temp_df = []
        #press_df = []
        #gnss_df = []
        print("Dataframes created successfully")
    except Exception as e:
        print("Error building dataframes", e)

    
    # Start each sensor collection in a new thread
    try:
        _thread.start_new_thread(dh.store_temperature, (temp_df,))
        print("Temperature thread running successfully")
    except Exception as e:
        print("Error creating temperature thread", e)

    #try:
    #    _thread.start_new_thread(dh.store_pressure, (press_df,))
    #    print("Pressure thread running successfully")
    #except Exception as e:
    #    print("Error creating pressure thread", e)
    
    #try:
    #    _thread.start_new_thread(dh.store_gnss, (gnss_df,))
    #    print("GNSS thread running successfully")
    #except Exception as e:
    #    print("Error creating GNSS thread", e)
    

    # Keep the main thread alive
    utime.sleep(5)
    global StopThread
    StopThread = True

if __name__ == "__main__":
    try:
        build_dataframes()
    except Exception as e:
        print("Error building dataframes", e)
        
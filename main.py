import utime
import _thread
from machine import Pin,UART
from machine import I2C
from ads1x15 import ADS1115
from max6675 import MAX6675

class DataHandling:
    def build_temp_dataframe(self):
        # Each entry is a tuple: (time, temp1, temp2, temp3, temp4)
        return []

    def build_press_dataframe(self):
        # Each entry is a tuple: (time, press1, press2, press3, press4)
        return []

    def build_gnss_dataframe(self):
        # Each entry is a tuple: (time, gnss)
        return []

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

    def collect_temp(self):
        try:
            # Use utime.localtime() to get the current time as a tuple.
            current_time = utime.localtime()
            temp1 = MAX6675(sck_pin=18, cs_pin=17, so_pin=16)
            #temp2 = MAX6675(sck_pin=18, cs_pin=20, so_pin=16)
            #temp3 = MAX6675(sck_pin=18, cs_pin=7, so_pin=16)
            #temp4 = MAX6675(sck_pin=18, cs_pin=6, so_pin=16)
            #return (current_time, temp1)
            return temp1
        except Exception as e:
            return None

    def collect_press(self):
        try:
            result = [None] * 5
            i2c = I2C(0, sda=Pin(12), scl=Pin(13))
            ads1 = ADS1115(i2c, address=0x48, gain=0)
            ads2 = ADS1115(i2c, address=0x49, gain=0)

            current_time = utime.localtime()
            value = ads1.read(4, 0)
            press1 = ads1.raw_to_v(value)
            value = ads2.read(4, 0)
            press2 = ads2.raw_to_v(value)

            return (current_time, press1, press2)
        except Exception as e:
            return None

    def collect_gnss(self):
        try:
            current_time = utime.localtime()
            gnss = UART(1,baudrate=9600,tx=Pin(4),rx=Pin(5),timeout=2000)
            return (current_time, gnss)
        except Exception as e:
            return None

    def store_temperature(self, df):
        while True:
            start = utime.ticks_ms()
            temp_data = self.collect_temp()
            if temp_data is not None:
                self.add_entry(df, temp_data)
            elapsed = utime.ticks_diff(utime.ticks_ms(), start)
            if elapsed < 500:
                utime.sleep_ms(500 - elapsed)
            print("Temperature Data:")
            print(temp_data)
            print()

    def store_pressure(self, df):
        while True:
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
        while True:
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
    try:
        temp_df = dh.build_temp_dataframe()
        #press_df = dh.build_press_dataframe()
        gnss_df = dh.build_gnss_dataframe()
        print("Dataframes created successfully")
    except Exception as e:
        print("Error building dataframes", e)

    # Start each sensor collection in a new thread
    try:
        _thread.start_new_thread(dh.store_temperature, (temp_df,))
        print("Temperature thread running successfully")
    except Exception as e:
        print("Error creating temperature thread", e)
    #_thread.start_new_thread(dh.store_pressure, (press_df,))
    '''
    try:
        _thread.start_new_thread(dh.store_gnss, (gnss_df,))
        print("GNSS thread running successfully")
    except Exception as e:
        print("Error creating GNSS thread", e)
    '''

    # Keep the main thread alive
    while True:
        utime.sleep(1)

if __name__ == "__main__":
    try:
        build_dataframes()
    except Exception as e:
        print("Error building dataframes", e)

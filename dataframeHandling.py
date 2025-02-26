import pandas as pd
import threading
import time
from datetime import datetime

class dataframeHandling:

    def buildTempDataframe(self):
        tempDF = pd.DataFrame(columns=["Time", "Temp1", "Temp2", "Temp3", "Temp4"])
        return tempDF

    def buildPressDataframe(self):
        pressDF = pd.DataFrame(columns=["Time", "Press1", "Press2", "Press3", "Press4"])
        return pressDF

    def buildGNSSDataframe(self):
        gnssDF = pd.DataFrame(columns=["Time", "GNSS"])
        return gnssDF

    def addEntry(self, dataFrame, values):
        df = pd.DataFrame([values], columns=dataFrame.columns)
        newDF = pd.concat([dataFrame, df], ignore_index=True)
        return newDF

    def getData(self, dataFrame, limit):
        storedData = []
        for index, row in dataFrame.iterrows():
            if len(storedData) < limit:
                storedData.append(row.tolist())
        return storedData

    def getSendIndicator(self):
        return True

    def clearDataframes(self, temp, press, gnss):
        indicator = self.getSendIndicator()
        if indicator:
            temp.drop(temp.index, inplace=True)
            press.drop(press.index, inplace=True)
            gnss.drop(gnss.index, inplace=True)

    def collectTemp(self):
        try:
            time = datetime.now()
            temp1 = 13
            temp2 = 14
            temp3 = 12.5
            temp4 = 13.5
            return time, temp1, temp2, temp3, temp4
        except Exception:
            pass

    def collectPress(self):
        try:
            time = datetime.now()
            press1 = 3.8
            press2 = 6.5
            press3 = 4.3
            press4 = 6.2
            return time, press1, press2, press3, press4
        except Exception:
            pass

    def collectGNSS(self):
        try:
            time = datetime.now()
            gnss = "3333.5555.6666.7777"
            return time, gnss
        except Exception:
            pass

    def storeTemperature(self, df):
        while True:
            start = time.time()
            tempData = self.collectTemp()
            df = self.addEntry(df, tempData)
            elapsed = time.time() - start
            time.sleep(max(0, 0.5 - elapsed))
            print(df)
            print()

    def storePressure(self, df):
        while True:
            start = time.time()
            pressData = self.collectPress()
            df = self.addEntry(df, pressData)
            elapsed = time.time() - start
            time.sleep(max(0, 0.5 - elapsed))
            print(df)
            print()

    def storeGNSS(self, df):
        while True:
            start = time.time()
            gnssData = self.collectGNSS()
            df = self.addEntry(df, gnssData)
            elapsed = time.time() - start
            time.sleep(max(0, 0.5 - elapsed))
            print(df)
            print()

def buildDataframes():
    matrixHandling = dataframeHandling()
    x = matrixHandling.buildTempDataframe()
    y = matrixHandling.buildPressDataframe()
    z = matrixHandling.buildGNSSDataframe()

    tempThread = threading.Thread(target=matrixHandling.storeTemperature, args=(x,))
    pressThread = threading.Thread(target=matrixHandling.storePressure, args=(y,))
    gnssThread = threading.Thread(target=matrixHandling.storeGNSS, args=(z,))
    tempThread.start()
    pressThread.start()
    gnssThread.start()


if __name__ == '__main__':
    buildDataframes()





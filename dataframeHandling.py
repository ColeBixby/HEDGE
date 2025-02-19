import pandas as pd
from dataRecorder import dataRecorder

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

def buildDataframes():
    matrixHandling = dataframeHandling()
    x = matrixHandling.buildTempDataframe()
    y = matrixHandling.buildPressDataframe()
    z = matrixHandling.buildGNSSDataframe()
    recorder = dataRecorder()
    tempData = dataRecorder.collectTemp(recorder)
    pressData = dataRecorder.collectPress(recorder)
    gnssData = dataRecorder.collectGNSS(recorder)
    x = matrixHandling.addEntry(x, tempData)
    y = matrixHandling.addEntry(y, pressData)
    z = matrixHandling.addEntry(z, gnssData)


if __name__ == '__main__':
    buildDataframes()





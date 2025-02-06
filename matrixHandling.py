class MatrixHandling:

    def buildTempMatrix(self):
        tempMatrix = [[None] * 5 for i in range(60)]
        return tempMatrix

    def buildPressMatrix(self):
        pressMatrix = [[None] * 5 for i in range(60)]
        return pressMatrix

    def buildGNSSMatrix(self):
        gnssMatrix = [[None] * 2 for i in range(30)]
        return gnssMatrix

    def addEntry(self, matrix, value):
        for i in range(len(matrix)):
            if matrix[i][0] == None:
                matrix[i] = value
                return

    def getData(self, matrix, limit):
        storedData = []
        for i in range(len(matrix)):
            if matrix[i][0] != None and len(storedData) < limit:
                storedData.append(matrix[i])
        return storedData

    def getSendIndicator(self):
        return True

    def clearMatrices(self, temp, press, gnss):
        indicator = self.getSendIndicator()
        if indicator == True:
            for i in range(len(temp)):
                temp[i] = [None] * 5

            for i in range(len(press)):
                press[i] = [None] * 5

            for i in range(len(gnss)):
                gnss[i] = [None] * 2

def buildMatrices():
    matrixHandling = MatrixHandling()
    x = matrixHandling.buildTempMatrix()
    y = matrixHandling.buildPressMatrix()
    z = matrixHandling.buildGNSSMatrix()

if __name__ == '__main__':
    buildMatrices()





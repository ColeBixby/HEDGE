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

    def getData(self, matrix):
        storedData = []
        for i in range(len(matrix)):
            if matrix[i][0] != None:
                storedData.append(matrix[i])
        return storedData


def buildMatrices():
    matrixHandling = MatrixHandling()
    x = matrixHandling.buildTempMatrix()
    y = matrixHandling.buildPressMatrix()
    z = matrixHandling.buildGNSSMatrix()

    matrixHandling.addEntry(x, [1,2,3,4,5])
    result = matrixHandling.getData(x)


    print(x)
    print(result)

if __name__ == '__main__':
    buildMatrices()





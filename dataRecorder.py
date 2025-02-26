from datetime import datetime

class dataRecorder:

    #Rather than collecting entire datetime we can collect just hour, minute, and second since we know
    #launch date
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
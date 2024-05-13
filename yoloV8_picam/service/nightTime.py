from datetime import datetime, time

class NightTime:
    def __init__(self):
        a=1
        
    def __del__(self):
        a=1
    
    def isNight(self):
        now=datetime.now().time()
        if now >= time(19,15) or now<=time(7,15):
            print("night")
            return True
        else:
            print("day")
            return False

        

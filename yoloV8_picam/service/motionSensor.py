import RPi.GPIO as GPIO

class MotionSensor:
    def __init__(self,pin=16):
        self.pin=pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN)
        
    def __del__(self):
        GPIO.cleanup()
    
    def detectMotion():
        return GPIO.input(self.pin)
        
        



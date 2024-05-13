import RPi.GPIO as GPIO
import time

class IRFlood:
    def __init__(self, pin=21,duraion=20):
        self.pin=pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        
        self.duration=20
        self.on=False
    def __del__(self):
        GPIO.cleanup()
    
    def on_ir(self):
        print("on IR")
        GPIO.output(self.pin,GPIO.LOW)
        self.on=True
        return self.on
    def off_ir(self):
        print("off IR")
        GPIO.output(self.pin,GPIO.HIGH)
        self.on=False
        return self.on
    def smartOn(self,duration=20):
        self.duration=duration
        self.on_ir()
        

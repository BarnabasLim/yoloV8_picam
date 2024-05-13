import RPi.GPIO as GPIO
import time

class SoundSensor:
    def __init__(self,pin=16):
        self.pin=pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN)
        
    def __del__(self):
        GPIO.cleanup()
    
    def detectSound(self, frame=5):
        soundDetected=False
        for i in range(frame):
            soundDetected=soundDetected or self.detectSoundFrame()
            if(soundDetected):
                print("Sound Detected")
            else:
                print("nothing")
            time.sleep(0.1)
        if(soundDetected):
            print("Sound Detected")
        else:
            print("nothing")
        return soundDetected
    
    def detectSoundFrame(self):
        return not GPIO.input(self.pin)
        

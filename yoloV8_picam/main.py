from utils.utils import detect_count, motion_detection,motion_detection2
from service.dataController import DataController
from service.irFlood import IRFlood
from service.soundSensor import SoundSensor
from service.nightTime import NightTime
from service.yoloDetector import YoloDetector
from picamera2 import Picamera2
from ultralytics import YOLO
from datetime import datetime, time
#import traceback

import numpy as np
import cv2

import argparse
from datetime import datetime
import time


with open("crash.logs","a") as logfile:
    msg='Date time: '+ datetime.now().strftime("%d%m%Y, %H:%M:%S") + "\n"
    logfile.write(msg)

ap = argparse.ArgumentParser()

ap.add_argument("-t", "--telegram",action="store_true", 
help="send results to telegram")
ap.add_argument("-w", "--wifibroadcast", action="store_true",
help="send results through wifibroadast")
ap.add_argument("-d", "--debug", action="store_true",
help="activate debug mode")
ap.add_argument("-l", "--light", action="store_true",
help="always allow flood light on")

args=vars(ap.parse_args())

#Start Camera
picam2=Picamera2()
picam2.preview_configuration.enable_lores()
picam2.configure("preview")
w,h = picam2.preview_configuration.lores.size
print("check", w, h, picam2.preview_configuration.lores.size)
picam2.start()

debug_mode=args.get("debug", True)
print("debug_mode", debug_mode)

light_mode=args.get("light", True)
print("light_mode", light_mode)

#Load Model
#model= YOLO('yolov8n.pt')
model= YoloDetector(debug_mode)

dataController=None

motion_detected=False
start_time=time.time()
curr_time=start_time
prev_time=curr_time
curr_img=picam2.capture_buffer("lores")
prev_img=curr_img

##IR Flood light
irFlood=IRFlood()

##Sound Sensor
soundSensor=SoundSensor()

##Night Time
nightTime=NightTime()

#for difference pic
curr_img_main=picam2.capture_array("main")
prev_img_main=curr_img_main

#system check
interval=10

curr_interval=int(datetime.now().minute/interval)
prev_interval=curr_interval

def CheckAlive():
    if(curr_interval!=prev_interval):
        if dataController:
            dataController.send_system_alive()
                    

try:
    while True:
        
        if motion_detected:
            
            #motion_detected mode
            if curr_time-start_time<120:
                if light_mode:
                    irFlood.on_ir()
                #20 sec object detection mode
                curr_time=time.time()
                
                img=picam2.capture_array("main")
                img=cv2.cvtColor(img,cv2.COLOR_RGBA2RGB)
                
                im,detected_item=model.detectMotion(img)
        
                #if debug_mode:
                #    print("Check img shape: ", np.array(img).shape,
                #        "n Check max: ", np.array(img).max())
                #results=model.predict(source=img)
                #detected_item=detect_count(results, debug_mode)
                #im=results[0].plot()
                #im=np.array(im)/255
        
                #if debug_mode:
                #    cv2.imshow("Check this out", im)
                if dataController==None or curr_time-prev_time>30:
                    prev_time=time.time()
                    if dataController:
                        dataController.step_end()
                    del dataController
                    dataController=None
                    dataController=DataController(True, False, debug_mode)
                else:
                    if dataController.step(detected_item, img=im):
                        start_time=time.time()
                        #curr_time=start_time
                        #prev_time=curr_time
                        
            else:
                #20 sec object detection mode end
                motion_detected=False
                
                if dataController:
                    dataController.step_end()
                del dataController
                dataController=None
                dataController=DataController(True, False, debug_mode)
                
                ##reset
                time.sleep(1)
                irFlood.off_ir()
                time.sleep(2)
                print("take before pic")
                prev_img=picam2.capture_buffer("lores")
                prev_img_main=picam2.capture_array("main")
        else:
            
            #system check
            curr_interval=int(datetime.now().minute/interval)
            CheckAlive()
            prev_interval=curr_interval
            
            #motion not detected mode
            curr_img=picam2.capture_buffer("lores")

            #for difference pic
            curr_img_main=picam2.capture_array("main")

            
            #threshod
            #motion_detection
            #Bright: 7
            #Dark: 25
            #Solution 1: remove noise for night
            #Solution 2: variable threshold based on time
            #Solution 3: variable threshold based on average intensity
            #Find a better motion sensor algo
            #threshold=7
            #if nightTime.isNight():
            #    threshold=25
            #else:
            #    threshold=7
            #motion_detected=motion_detection(curr_img,prev_img,w, h,25,debug_mode)
            #motion_detected=motion_detected or soundSensor.detectSound()
            #motion_detected=False
            motion_detected, curr_cpy=motion_detection2(curr_img_main,prev_img_main,debug_mode)
            if(motion_detected):
                #First time motion detected
                start_time=time.time()
                curr_time=start_time
                prev_time=curr_time
                
                
                if dataController:
                    dataController.step_end()
                del dataController
                dataController=None
                dataController=DataController(True, False, debug_mode)
                
                
                img=picam2.capture_array("main")
                img=cv2.cvtColor(img,cv2.COLOR_RGBA2RGB)
                img=img/255
                dataController.step_start(img)
                
                dataController.step_start(curr_cpy*255)
            else:
                a=1
                time.sleep(0.5)
            prev_img=curr_img
            prev_img_main=curr_img_main
            
            
        if(cv2.waitKey(25) & 0xFF == ord("q")):
            if(dataController!=None):
                del dataController
            if(irFlood!=None):
                del irFlood
            if(soundSensor!=None):
                del soundSensor
            cv2.destroyAllWindows()
            break
except Exception as e:
    with open("crash.logs","a") as logfile:
        msg='Error Date time: '+ datetime.now().strftime("%d%m%Y, %H:%M:%S") + "\n"
        logfile.write(msg)
        logfile.write(str(e))
        
        #traceback.print_exc(file=logfile)

    
    
    
            

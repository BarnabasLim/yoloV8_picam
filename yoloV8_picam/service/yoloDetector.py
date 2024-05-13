from ultralytics import YOLO
import cv2
import numpy as np

class YoloDetector:
	def __init__(self, debug_mode=False):
		#Load Model
		self.debug_mode=debug_mode
		self.model=YOLO('yolov8n.pt')
		
	def __del__(self):
		a=1
		
	def detectMotion(self,img):
		results=self.model.predict(source=img)
		detected_item=self.detect_count(results)
		im=results[0].plot()
		im=np.array(im)/255
		if self.debug_mode:
			cv2.imshow("Check this out", im)
		return im,detected_item
	
	def detect_count(self,results):
		detected_item={}
		class_id=results[0].boxes.cls.cpu().numpy().astype(int)
		names=results[0].names
		
		for i in class_id:
			if names[i] in detected_item:
				detected_item[names[i]]=detected_item[names[i]]+1
			else:
				detected_item[names[i]]=1
				
		if(self.debug_mode):
			print(detected_item)
		return detected_item

import numpy as np
import copy
import cv2

def detect_count(results, debug_mode=False):
    detected_item={}
    class_id=results[0].boxes.cls.cpu().numpy().astype(int)
    names=results[0].names
    
    for i in class_id:
        if names[i] in detected_item:
            detected_item[names[i]]=detected_item[names[i]]+1
        else:
            detected_item[names[i]]=1
    if(debug_mode):
        print(detected_item)
    return detected_item
    
def cat(file_path):
    print(file_path)
    try: 
        with open(file_path,'rb') as file:
            content=file.read()
            print(f"image_file: {file_path}")
            print(content)
            print(type(content))
    except FileNotFoundError:
        print(f"File not found: {file_path}")

def motion_detection(curr, prev,w,h, threshold=7, debug=False):
    #Measure pixel differences between current and previous frames
    curr=curr[:w*h].reshape(h,w)
    prev=prev[:w*h].reshape(h,w)
    mse=np.square(np.subtract(curr,prev)).mean()
    if(debug):
        print("motion_detection", mse)
    if mse > threshold:
        return True
    else:
        return False

def motion_detection2(curr, prev,debug=False):
    curr_cpy=copy.deepcopy(curr)
    
    diff=cv2.absdiff(curr,prev)
    gray=cv2.cvtColor(diff,cv2.COLOR_BGR2GRAY)
    blur=cv2.GaussianBlur(gray, (13,13),0)
    _,thresh=cv2.threshold(blur,10,255,cv2.THRESH_BINARY)
    dilate=cv2.dilate(thresh,None,iterations=5)
    contours,_= cv2.findContours(dilate, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    
    valid_contours=[]
    for contour in contours:
        (x,y,w,h)=cv2.boundingRect(contour)
        if cv2.contourArea(contour)>700:
            valid_contours.append([x,y,w,h])
            cv2.rectangle(curr_cpy, (x,y),(x+w,y+h),(0,255,0),2)
    #cv2.drawContours(curr_cpy, contours,-1,(255,0,0),4)
    #cv2.imshow("feed",curr_cpy)
    
    return len(valid_contours)>0, curr_cpy
        

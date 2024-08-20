import sys
import io
import PIL.Image as Image
import re
import os
import cv2
def write_binary_to_jpg(file_path,content):
    try:
        write_path=file_path.replace("captured_vehicle/", "/home/barns/Desktop/")
        ## d_%d_%m_%Y_t_%H_%M_%S
        write_path=re.sub(r'_t_(\d+)_', r'_t_\1/t_\1_',write_path)
        os.makedirs(os.path.dirname(write_path),exist_ok=True)
        with open(write_path,'wb') as file:
            content=eval(content)
            file.write(content)
        #image show
        image=cv2.imread(write_path) 
        cv2.imshow("Detection", image)
        print(f"jpg success")
    except  Exception as e:
        print("Error writing jpg :",e)
n=0
while True:
    user_in=input()
    if user_in:
        print(f"{n} line Barn: {user_in}")
        if user_in.startswith("image_file: "):
            file_path=user_in.replace("image_file: ","")
            content=input()
            if content:
                write_binary_to_jpg(file_path, content)
        n=n+1

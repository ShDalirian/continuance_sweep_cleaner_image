import cv2
import numpy as np
import pandas as pd


def continuance_image_cleaner(img,text_pixel_ratio:int=20,symbol_pixel_ratio:int=70,x_step:int=18,y_step:int=25,is_background_white:bool=True, crop_around:bool=True):
    #split image to sub boxes and delete some ratio part
    if is_background_white:
        cleaned_img=255*np.ones((img.shape[0],img.shape[1]),dtype=np.uint8)
    else:
        cleaned_img=np.zeros((img.shape[0],img.shape[1]),dtype=np.uint8)
    x_step:int=min(img.shape[1]//3,x_step)
    y_step:int=min(img.shape[0]//3,y_step)
    if img.shape[2]>1:
        img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    for y in range(0,img.shape[0]-y_step):
        for x in range(0,img.shape[1]-x_step):
            black_count:int=0
            white_count:int=0
            window=img[y:y+y_step,x:x+x_step]
            white_count =window[window>=250].size
            black_count =window[window<=50].size
            total_pixel=x_step*y_step
            b_w_ratio:float=black_count/total_pixel
            w_b_ratio:float=white_count/total_pixel
            if (is_background_white and b_w_ratio>text_pixel_ratio/100 and b_w_ratio<symbol_pixel_ratio/100) or (~is_background_white and w_b_ratio>text_pixel_ratio/100 and w_b_ratio<symbol_pixel_ratio/100):
                    cleaned_img[y:y+y_step,x:x+x_step]=img[y:y+y_step,x:x+x_step]
    return cleaned_img
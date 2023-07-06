
import time
import cv2
import numpy as np
import urllib.request
from LogFunctions import *

rectanglesize = 50
crop_y=200
crop_x=200
crop_h=rectanglesize + crop_y
crop_w=rectanglesize + crop_x
contrastvalues = []
maxcontrast_val = 0
maxcontrast_index = 0

def url_to_image(url):
	# download the image, convert it to a NumPy array, and then read
	# it into OpenCV format
	resp = urllib.request.urlopen(url)
	image = np.asarray(bytearray(resp.read()), dtype="uint8")
	image = cv2.imdecode(image, cv2.IMREAD_COLOR)
	# return the image
	return image

def getcontrast(image):
    # convert to LAB color space
    lab = cv2.cvtColor(image,cv2.COLOR_BGR2LAB)

    # separate channels
    L,A,B=cv2.split(lab)

    # compute minimum and maximum in 5x5 region using erode and dilate
    kernel = np.ones((5,5),np.uint8)
    min = cv2.erode(L,kernel,iterations = 1)
    max = cv2.dilate(L,kernel,iterations = 1)

    # convert min and max to floats
    min = min.astype(np.float64) 
    max = max.astype(np.float64) 

    # compute local contrast
    contrast = (max-min)/(max+min)

    # get average across whole image
    average_contrast = 100*np.mean(contrast)
    return average_contrast

def getcurrentframe():
    return url_to_image('http://192.168.1.62:8080/snapshot')

def changefocus(cameracontrol, focalvalue, x, y):
    global display_image, current_focalvalue
    Logger.LogInfo("Changing focus {}".format(focalvalue))

    int_focalvalue = int(65535 * focalvalue)

    cameracontrol.onFocusPullSetInt(int_focalvalue)

    Logger.LogInfo("Changed lens focus, grabbing frame from camera")

    time.sleep(0.3)
    display_image = getcurrentframe()
    # display_image = vid.read()

    Logger.LogInfo("Changed lens focus, frame grabbed, copying image")

    crop_image = display_image.copy()

    Logger.LogInfo("Image copied, now calculating contrast from focus rectangle")

    x_start = int(x - (rectanglesize / 2))
    x_end = int(x + (rectanglesize / 2))
    y_start = int(y - (rectanglesize / 2))
    y_end = int(y + (rectanglesize/2))
    crop_image = crop_image[x_start:x_end, y_start:y_end]
    contrast = getcontrast(crop_image)
    current_focalvalue = focalvalue
    return contrast

def autofocuspass(cameracontrol, x, y, start, stop, step, plot=False):
    maxcontrast_value = None
    maxcontrast_index = None
    if plot: contrastvalues = []

    for index in range (int(start / step), 1 + int(stop / step)):
        i = float(index * step)
        contrast = changefocus(cameracontrol, i, x, y)
        if plot: contrastvalues.append(contrast)
        if maxcontrast_value is None:
            maxcontrast_value = contrast
            maxcontrast_index = i
        else:
            if contrast > maxcontrast_value:
                maxcontrast_value = contrast
                maxcontrast_index = i
            
    Logger.LogInfo("Maximum contrast on step {} with range {} {} {}".format(step, start, stop, maxcontrast_index))

    return maxcontrast_index

def autofocus(cameracontrol, x, y):
    step_pass = 0.1
    maxcontrast_start, maxcontrast_stop = 0, 1
    Logger.LogInfo("******** Starting auto focus **********")

    for i  in range(3):
        maxcontrast_pass = autofocuspass(cameracontrol, x, y, maxcontrast_start, maxcontrast_stop, step_pass)
        maxcontrast_start = maxcontrast_pass - step_pass
        maxcontrast_stop = maxcontrast_pass + step_pass
        if maxcontrast_start < 0: maxcontrast_start = 0
        if maxcontrast_stop > 1: maxcontrast_stop = 1
        step_pass = (step_pass / 10)

    changefocus(cameracontrol, maxcontrast_pass, x, y)

    print("******** Finished auto focus **********")
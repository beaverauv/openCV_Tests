import sys
import copy
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2

#This algo can detect # of posts
#Primarily looks at the red channel since the posts
#stick out like a sore thumb compared to green and blue

#So far so good... Issues:
#Mask is based off of 90th percentile...
#Good for far away mix, but up close doesn't work
#Need algo to extract outliers in terms of color

#Blog detection is good, but the interia term doesn't work
#It supposed is a measurement of the flatness (circle v line)
#Could be good identifier

def rgb_channel_scale(img, red, green, blue): #Actually B, G, R, too lazy to move around
	b, g, r = cv2.split(img)
	npr = np.array(r) * red
	npg = np.array(g) * green
	npb = np.array(b) * blue
	return cv2.merge((npb, npg, npr))

if len(sys.argv) != 3:
	print("This test requires arguements: python test2.py [path_to_image (string)] [debug (bool)]")
	print("Exiting...")
	sys.exit()

debug = sys.argv[2]
img = cv2.imread(sys.argv[1], 1)
cv2.imshow("img", img) 

blur = cv2.bilateralFilter(img, 9, 75, 75)

blue, green, red = cv2.split(blur)

#redhsv = cv2.cvtColor(cv2.cvtColor(red, cv2.COLOR_GRAY2RGB), cv2.COLOR_RGB2HSV)

#lower_red = np.array([0,0,int(np.percentile(red, 85))])
#upper_red = np.array([0,0,255])

#mask = cv2.inRange(redhsv, lower_red, upper_red)

#res = cv2.bitwise_and(red,red, mask= mask)

# Setup SimpleBlobDetector parameters.
params = cv2.SimpleBlobDetector_Params()
 
# Change thresholds
params.minThreshold = 0;
params.maxThreshold = 255;
 
# Filter by Area.
params.filterByArea = True
params.minArea = 250
 
# Filter by Circularity
params.filterByCircularity = False
params.minCircularity = 0.1
 
# Filter by Convexity
params.filterByConvexity = False
params.minConvexity = 0.8
 
# Filter by Inertia
params.filterByInertia = False
params.maxInertiaRatio = 1
 
# Create a detector with the parameters
ver = (cv2.__version__).split('.')
if int(ver[0]) < 3 :
    detector = cv2.SimpleBlobDetector(params)
else : 
    detector = cv2.SimpleBlobDetector_create(params)
#cv2.imshow("mask",mask)

keypoints = detector.detect(255-red)
#keypoints = detector.detect(255-mask)

print("I believe there are " + str(len(keypoints)) + " Poles")

img_keypoints = np.empty((img.shape[0], img.shape[1], 3), dtype=np.uint8)
red_keypoints = np.empty((img.shape[0], img.shape[1], 3), dtype=np.uint8)
cv2.drawKeypoints(img, keypoints, img_keypoints)
cv2.drawKeypoints(red, keypoints, red_keypoints)
#-- Show detected (drawn) keypoints
cv2.imshow('Keypoints', img_keypoints)
cv2.imshow("red keypoints", red_keypoints)

#cv2.imshow('final', detector)


cv2.waitKey(0)
cv2.destroyAllWindows()

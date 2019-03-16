#This algo is to determine the number of posts
#It works by using blob detection on the red channel
#Also has a few other things to discriminate

#ARGUEMENTS:
#img - (np array), the image in bgr format to check
#debug - (bool) [False], whether there is an ouput for the steps

#RETURNS:
#int - the number of poles

#NOTE: TRY FILTERING BY KEYPOINT.SIZE, ie we expect 2 to be similar

import sys
import copy
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2

def execute(img, debug=False):
	blur = cv2.bilateralFilter(img, 9, 75, 75)

	blue, green, red = cv2.split(blur)

	# Setup SimpleBlobDetector parameters.
	params = cv2.SimpleBlobDetector_Params()

	# Change thresholds
	params.minThreshold = 20;
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

	keypoints = detector.detect(255-red)
	for k in keypoints:
		print(k.octave)

	if debug == True:
		img_keypoints = np.empty((img.shape[0], img.shape[1], 3), dtype=np.uint8)
		red_keypoints = np.empty((img.shape[0], img.shape[1], 3), dtype=np.uint8)
		cv2.drawKeypoints(img, keypoints, img_keypoints)
		cv2.drawKeypoints(red, keypoints, red_keypoints)
		#-- Show detected (drawn) keypoints
		cv2.imshow('Keypoints', img_keypoints)
		cv2.imshow("red keypoints", red_keypoints)

	return len(keypoints)


#Allows the file to be executed and tested on its own
if __name__ == "__main__":
	if len(sys.argv) != 3:
		print("This test requires arguements: python test2.py [path_to_image (string)] [debug (bool)]")
		print("Exiting...")
		sys.exit()

	if sys.argv[2] == "True":
		debug = True
	else:
		debug = False

	img = cv2.imread(sys.argv[1], 1)

	if debug == True:
		cv2.imshow("img", img)
	print("I believe there are " + str(execute(img, debug)) + " poles")
	cv2.waitKey(0)
	cv2.destroyAllWindows()

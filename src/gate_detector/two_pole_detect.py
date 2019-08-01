#This algo is good at detecting between two posts
#Not at all useful for one post, so must be after number poles function
#If Kmeans fails, it will return everything normally except -1 as the middle location

#ARGUEMENTS:
#img - (np array), the image in bgr format to check
#debug - (bool) [False], whether there is an ouput for the steps

#RETURNS:
#int, float, np.arry
#number of pixels wide
#x coord of the middle
#the resulting image with gate highlighted

import sys
import copy
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2

def execute(img, debug=False):
	def gbr_channel_scale(img, red, green, blue): #Actually B, G, R
		r, g, b = cv2.split(img)
		npr = np.array(r) * red
		npg = np.array(g) * green
		npb = np.array(b) * blue
		return cv2.merge((npr, npg, npb))

	hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

	cv2.imshow('hsv', hsv)    
	lower_red = np.array([19,50,100])
	upper_red = np.array([23,130,255])
	mask = cv2.inRange(hsv, lower_red, upper_red)
	res = cv2.bitwise_and(hsv,hsv, mask= mask)
	cv2.imshow('mask', res)

	boosted_img = gbr_channel_scale(img, 0, 0, 1)
	kernel = np.ones((7,7), np.uint8)
	opened =  cv2.morphologyEx(boosted_img, cv2.MORPH_OPEN, kernel)

	blur = cv2.bilateralFilter(opened, 9, 75, 75)

	b, g, r = cv2.split(blur)

	t, thres = cv2.threshold(r, 65, 255, cv2.THRESH_TOZERO)

	cv2.imshow('threshold', thres)
#	v = np.median(r)
#	print v
#	sigma = 1.0
#	lower = int(max(0, (1.0-sigma)*v))
#	upper = int(min(255, (1.0+sigma)*v))

#	print lower, upper


	edges = cv2.Canny(thres, 127, 255)

	lines = cv2.HoughLinesP(edges, rho=6, theta=np.pi / 60, threshold=100, lines=np.array([]), minLineLength=70, maxLineGap=35)
	verticallines = []
	horizontallines = []

	if debug == True:
		linesImage = copy.copy(img)
	if lines is not None:
		for line in lines:
			for x1, y1, x2, y2 in line:
				slope = float(y2-y1) / (x2-x1)
				if abs(slope) > 1:
					verticallines.append(line)
					if debug == True:
						cv2.line(linesImage, (x1,y1), (x2,y2), (255,255,255), 3)
				else:
					horizontallines.append(line)
					if debug == True:
						cv2.line(linesImage, (x1,y1), (x2,y2), (0,0,0), 3)

		floatLines = np.float32(verticallines)

		# define criteria and apply kmeans()
		criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
		try:
			ret,label,center=cv2.kmeans(floatLines,2,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)
		except Exception as e:
			print("K Means Failed: Returning to advoid crash...")
			print(e)
			return img.shape[1], -1, img

		topLeft = None
		topRight = None

		if center[0][1] < center[0][3]:
			topLeft = 1
		else:
			topLeft = 3

		if center[1][1] < center[1][3]:
			topRight = 1
		else:
			topRight = 3

		cv2.line(img, (center[0][topLeft-1],center[0][topLeft]), (center[1][topRight-1],center[1][topRight]), (0,0,255), 3)
		cv2.line(img, (center[0][0],center[0][1]), (center[0][2],center[0][3]), (255,0,0), 3)
		cv2.line(img, (center[1][0],center[1][1]), (center[1][2],center[1][3]), (0,255,0), 3)

		cv2.circle(img, (center[0][0], center[0][1]), 5, (255,255,255), -1)
		cv2.circle(img, (center[0][2], center[0][3]), 5, (255,255,255), -1)
		cv2.circle(img, (center[1][0], center[1][1]), 5, (255,255,255), -1)
		cv2.circle(img, (center[1][2], center[1][3]), 5, (255,255,255), -1)
	
	if debug == True:
		cv2.imshow("boosted", boosted_img)
		cv2.imshow('opening', opened)
		cv2.imshow('thres', thres)
		cv2.imshow("canny", edges)
		cv2.imshow("lines", linesImage)
		cv2.imshow('final',img)

	if lines is not None:
		return img.shape[1], int((center[0][topLeft-1] + center[1][topRight-1])/2)
	else:
		return None

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

	print(execute(img, debug))

	cv2.waitKey(0)
	cv2.destroyAllWindows()

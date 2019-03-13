import sys
import copy
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2


#This algo is good at detecting between two posts
#Not at all useful for one post


def gbr_channel_scale(img, red, green, blue): #Actually B, G, R
	r, g, b = cv2.split(img)
	npr = np.array(r) * red
	npg = np.array(g) * green
	npb = np.array(b) * blue
	return cv2.merge((npr, npg, npb))

if len(sys.argv) != 3:
	print("This test requires arguements: python test2.py [path_to_image (string)] [debug (bool)]")
	print("Exiting...")
	sys.exit()

debug = sys.argv[2]
img = cv2.imread(sys.argv[1], 1)
cv2.imshow("img", img) 

gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

boosted_img = gbr_channel_scale(img, 1, 2, 3)
if debug == "True":
	cv2.imshow("boosted", boosted_img)


edges = cv2.Canny(boosted_img, 50,150,apertureSize = 3)
if debug == "True":
	cv2.imshow("canny", edges)



lines = cv2.HoughLinesP(edges, rho=6, theta=np.pi / 60, threshold=160, lines=np.array([]), minLineLength=60, maxLineGap=25)
verticallines = []
horizontallines = []

linesImage = copy.copy(img)

for line in lines:
	for x1, y1, x2, y2 in line:
		slope = float(y2-y1) / (x2-x1)
		if abs(slope) > 1:
			verticallines.append(line)
			cv2.line(linesImage, (x1,y1), (x2,y2), (255,255,255), 3)
		else:
			horizontallines.append(line)
			cv2.line(linesImage, (x1,y1), (x2,y2), (0,0,0), 3)
if debug == "True":
	cv2.imshow("lines", linesImage)

floatLines = np.float32(verticallines)

# define criteria and apply kmeans()
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
ret,label,center=cv2.kmeans(floatLines,2,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)

# Now separate the data, Note the flatten()
A = floatLines[label.ravel()==0]
B = floatLines[label.ravel()==1]

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

cv2.imshow('final',img)

cv2.waitKey(0)
cv2.destroyAllWindows()

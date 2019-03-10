import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2

def gbr_channel_scale(img, red, green, blue): #Actually G, B, R
	r, g, b = cv2.split(img)
	npr = np.array(r) * red
	npg = np.array(g) * green
	npb = np.array(b) * blue
	return cv2.merge((npr, npg, npb))

img = cv2.imread('10.jpg', 1)
cv2.imshow("img", img) 

gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

boosted_img = gbr_channel_scale(img, 2, 1, 3)
cv2.imshow("boosted", boosted_img)


edges = cv2.Canny(boosted_img,50,150,apertureSize = 3)
cv2.imshow("canny", edges)



#lines = cv2.HoughLines(edges, 1, np.pi/180,200)
lines = cv2.HoughLinesP(edges, rho=6, theta=np.pi / 60, threshold=160, lines=np.array([]), minLineLength=40, maxLineGap=25)
verticallines = []
horizontallines = []

for line in lines:
	for x1, y1, x2, y2 in line:
		slope = float(y2-y1) / (x2-x1)
		if abs(slope) > 1:
			verticallines.append(line)
			cv2.line(img, (x1,y1), (x2,y2), (255,255,255), 3)
		else:
			horizontallines.append(line)
			#cv2.line(img, (x1,y1), (x2,y2), (0,0,0), 3)

x = []
y = []
print(verticallines[:][0])
for lines in verticallines:
	x.append(lines[0][0])
	y.append(lines[0][1])
	x.append(lines[0][2])
	y.append(lines[0][3])
print('x: ', x)
print('y: ', y)

test_poly = np.poly1d(np.polyfit(x, y, 1))
cv2.line(img, (0,int(test_poly(0))), (img.shape[1], int(test_poly(img.shape[1]))), (0,0,0), 5)

cv2.imshow('houghlines3',img)

cv2.waitKey(0)
cv2.destroyAllWindows()

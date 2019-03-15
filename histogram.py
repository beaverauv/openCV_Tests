import sys
import copy
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2

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

cv2.imshow('red',red)
plt.hist(red.ravel(),256,[0,256]); plt.show()

cv2.waitKey(0)
cv2.destroyAllWindows()

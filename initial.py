import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2

#-----Reading the image-----------------------------------------------------
img = cv2.imread('1.jpg', 1)
cv2.imshow("img",img) 

#-----Converting image to LAB Color model----------------------------------- 
lab= cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
#cv2.imshow("lab",lab)

#-----Splitting the LAB image to different channels-------------------------
l, a, b = cv2.split(lab)
#cv2.imshow('l_channel', l)
#cv2.imshow('a_channel', a)
#cv2.imshow('b_channel', b)

#-----Applying CLAHE to L-channel-------------------------------------------
clahe = cv2.createCLAHE(clipLimit=8.0, tileGridSize=(8,16))
cl = clahe.apply(l)
#cv2.imshow('CLAHE output', cl)

#-----Merge the CLAHE enhanced L-channel with the a and b channel-----------
limg = cv2.merge((cl,a,b))
#cv2.imshow('limg', limg)

#-----Converting image from LAB Color model to RGB model--------------------
final = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
cv2.imshow('final', final)

#_____END_____#


'''img = cv2.imread('1.jpg', 1)
cv2.imshow('Original',img)
edges = cv2.Canny(img, 100, 200)
cv2.imshow('Canny', edges)

color_boost = channel_boost(img, 2, 2, 2)
cv2.imshow('Boosted', color_boost)
'''
cv2.waitKey(0)
cv2.destroyAllWindows()

"""plt.subplot(121), plt.imshow(img, cmap = 'brg')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(1221), plt.imshow(edges, cmap = 'brg')
plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

plt.show()
"""


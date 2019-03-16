import gate_detector.number_poles as numpoles
import gate_detector.two_pole_detect as twopole
import cv2
import time
import sys


start = time.time()

img = cv2.imread(sys.argv[1], 1)

if numpoles.execute(img) == 2:
	width, coord, img = twopole.execute(img)
	print(width, coord)
	cv2.imshow("Detected", img)
else:
	print("Not 2 Poles")


end = time.time()
print("You could use around " + str(int(1/(end-start))) + " FPS")

cv2.waitKey(0)
cv2.destroyAllWindows()

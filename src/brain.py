import gate_detector.number_poles as numpoles
import cv2

img = cv2.imread('../photos/1.jpg', 1)

print(numpoles.execute(img))

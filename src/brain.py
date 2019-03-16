import gate_detector.number_poles as numpoles
import gate_detector.two_pole_detect as twopole
import cv2
import time

img = cv2.imread('../photos/1.jpg', 1)

start = time.time()
print(twopole.execute(img))
end = time.time()
print("You could use around " + str(int(1/(end-start))) + " FPS")

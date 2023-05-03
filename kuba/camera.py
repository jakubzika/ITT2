import cv2 as cv
import numpy as np

cap = cv.VideoCapture("udp://0.0.0.0:1234")
# cap = cv.VideoCapture(0)


while True:
    ret, img2 = cap.read()
    print("read frame")

    cv.imshow('img', img2)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# After the loop release the cap object
cap.release()
# Destroy all the windows
cv.destroyAllWindows()

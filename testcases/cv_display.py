# https://learnopencv.com/read-display-and-write-an-image-using-opencv/

import cv2

image1 = cv2.imread('Beautiful_Red_Rose.jpeg')
cv2.imshow('Window 2', image1)
print(image1.shape)
cv2.waitKey(0)

cv2.destroyAllWindows()


import cv2

image = cv2.imread('bp.png')

cv2.line(image, (1600,300), (1600,1000), (255,0,255),thickness=5)
cv2.circle(image, (1850,980), 100, (255,255,0), thickness=5)
cv2.putText(image, 'Correct', (100,300), 16, 6, (255,255,255), thickness=5)

cv2.imshow('Window 1', image)
print(image.shape)
cv2.waitKey(0)

# cv2.imread() - open an image from a file
# cv2.imshow() - display an image
# cv2.imwrite() - save an image as a file
# cv2.imwrite("Name of the file", image you want to save)
cv2.imwrite('edited.png', image)
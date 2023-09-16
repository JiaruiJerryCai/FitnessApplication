import pose_detector # should be able to give back coordinates of body parts, angle of joints, distance of points, slope of points
import cv2

# https://developers.google.com/mediapipe/solutions/vision/pose_landmarker

file_name = "testcases/VideosandPhotos/a.png"
image = cv2.imread(file_name)

# create the body detector object
detector = pose_detector.Detector()

newImage = detector.analyze(image)
cv2.imshow("Image", image)

print(detector.getAngle(12,14,16)) # testcase

cv2.waitKey(0)


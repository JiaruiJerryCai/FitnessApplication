import cv2
import mediapipe

file_location="testcases/a.png"

# Read and display bp.png from file
pic = cv2.imread(file_location)
print(pic.shape)
cv2.imshow('a',pic)
cv2.waitKey(0)

# Setup tools neccessary for using mediapipe
mp_drawing = mediapipe.solutions.drawing_utils
mp_pose = mediapipe.solutions.pose
pose = mp_pose.Pose()   # Store POSE AI model inside variable

# Convert image from opencv (BGR) to mediapipe (RGB)
rgbPic = cv2.cvtColor(pic, cv2.COLOR_BGR2RGB)

result = pose.process(rgbPic) # use model to analyze the given image

# Use mp_drawing to draw out final results on rgbPic
mp_drawing.draw_landmarks(pic, result.pose_landmarks, mp_pose.POSE_CONNECTIONS)

# Display the edited rgbPic
cv2.imshow("body analysis",pic)
cv2.waitKey(0)







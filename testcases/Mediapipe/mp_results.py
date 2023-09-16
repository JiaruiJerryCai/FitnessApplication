import mediapipe
import cv2

file_location="testcases/VideosandPhotos/a.png"

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

print(result) # Object containing data
print("====================================")
print(result.pose_landmarks)    # List of all body parts
print("====================================")
print(result.pose_landmarks.landmark[14])   # List Coordinates of Specific Body Parts
print("====================================")
print(result.pose_landmarks.landmark[14].x) # X value of body part
print(result.pose_landmarks.landmark[14].y) # Y value of body parts



# Use mp_drawing to draw out final results on rgbPic
mp_drawing.draw_landmarks(pic, result.pose_landmarks, mp_pose.POSE_CONNECTIONS)

# Display the edited rgbPic
cv2.imshow("body analysis",pic)
cv2.waitKey(0)



import cv2
import mediapipe

# Get the video from the file
video = cv2.VideoCapture(0) # Change the file name to 0 to read the webcam

# Setup tools neccessary for using mediapipe
mp_drawing = mediapipe.solutions.drawing_utils
mp_pose = mediapipe.solutions.pose
pose = mp_pose.Pose()   # Store POSE AI model inside variable

if not video.isOpened():
    print("Error with video file...")

# Check if the video is open
while video.isOpened():

    # Read the next frame of the video
    success, frame = video.read()

    if success:

        # Convert image from opencv (BGR) to mediapipe (RGB)
        rgbPic = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        result = pose.process(rgbPic) # use model to analyze the given image

        # Use mp_drawing to draw out final results on rgbPic
        mp_drawing.draw_landmarks(frame, result.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # cv2.circle(frame, (frame.shape[1]//2, frame.shape[0]//2), 100, (255,255,0), thickness=5)

        cv2.imshow("Video 1", frame)
        key = cv2.waitKey(100)

        if key == ord('q'):
            break


    else:
        break

video.release()
cv2.destroyAllWindows()





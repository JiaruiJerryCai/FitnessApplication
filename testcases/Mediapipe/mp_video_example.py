import cv2
import mediapipe


mp_drawing = mediapipe.solutions.drawing_utils
mp_pose = mediapipe.solutions.pose
pose = mp_pose.Pose()


# Get the video from the file
video = cv2.VideoCapture('testcases/run.mp4') # Change the file name to 0 to read the webcam

if not video.isOpened():
    print("Error with video file...")

# Check if the video is open
while video.isOpened():

    # Read the next frame of the video
    success, frame = video.read()

    if success:

        rgbFrame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        result = pose.process(rgbFrame)
        mp_drawing.draw_landmarks(frame,result.pose_landmarks,mp_pose.POSE_CONNECTIONS)

        cv2.imshow("Workout", frame)
        key = cv2.waitKey(100)

        if key == ord('q'):
            break

    else:
        break

video.release()
cv2.destroyAllWindows()





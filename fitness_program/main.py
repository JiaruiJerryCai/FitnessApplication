import cv2
import mediapipe
import Pullup
import Pushup

# Get the video from the file
file_location = 'fitness_program/Pullup.mp4'
video = cv2.VideoCapture(file_location) # Change the file name to 0 to read the webcam

if not video.isOpened():
    print("Error with video file...")

# pushupAnalyzer = Pushup.set()
pullupAnalyzer = Pullup.set()

# Check if the video is open
while video.isOpened():

    # Read the next frame of the video
    success, frame = video.read()

    if success:
        # Progess the rep based on the frame
        pullupAnalyzer.process(frame)

        cv2.imshow("Your Workout", frame)
        key = cv2.waitKey(0)
        if key == ord('q'):
            break

    else:
        break

video.release()
cv2.destroyAllWindows()

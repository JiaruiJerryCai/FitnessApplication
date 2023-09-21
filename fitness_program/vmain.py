import cv2
import mediapipe
import pose_detector

# create the body detector object
detector = pose_detector.Detector()

# Get the video from the file
video = cv2.VideoCapture('fitness_program/pushup_incorrect.mp4') # Change the file name to 0 to read the webcam

if not video.isOpened():
    print("Error with video file...")

count = 0 
direction = 0 # going up is 1 and down is 0 
isFormCorrect = True

# Check if the video is open
while video.isOpened():

    # Read the next frame of the video
    success, frame = video.read()

    if success:

        # Gather information about push up pose
        detector.analyze(frame)
        angleofleftelbow = detector.getAngle(15, 13, 11)
        angleofleftbutt = detector.getAngle(25, 23, 11)
        angleofleftknee = detector.getAngle(23, 25, 27)

        # To check arms, confirm if elbows past 90 degrees and extend past 150
        if direction == 0: # the user is going down
            if angleofleftelbow < 80:
                direction = 1
        elif direction == 1: # the user is going up
            if angleofleftelbow > 140:
                direction = 0 
            
        # To check the back angle
        if angleofleftbutt > 150 and angleofleftbutt < 190:
            pass
        else:
            print("Bad back")

        # Head: get points of the back to find line of best fit then detect if head position is in the line
        if angleofleftknee > 145:
            pass
        else:
            print("Bad knee")

        cv2.putText(frame, str(count), (100,300), 16, 3, (0,0,255), thickness=5)

        cv2.imshow("Your Workout", frame)
        key = cv2.waitKey(0)

        if key == ord('q'):
            break

    else:
        break

video.release()
cv2.destroyAllWindows()

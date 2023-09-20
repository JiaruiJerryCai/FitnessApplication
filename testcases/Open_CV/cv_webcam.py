import cv2

# Get the video from the file
video = cv2.VideoCapture(0) # Change the file name to 0 to read the webcam

# Check if the video is open
while video.isOpened():

    # Read the next frame of the video
    success, frame = video.read()

    if success:
        cv2.imshow("Video 1", frame)
        key = cv2.waitKey(100)

        if key == ord('q'):
            break


    else:
        break

video.release()
cv2.destroyAllWindows()





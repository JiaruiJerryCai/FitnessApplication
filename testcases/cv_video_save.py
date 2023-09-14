'''
## Session 3: Saturday 9/9

Git and GitHub practice
- create and upload readme
- try different interactions

Learning Open CV
- https://learnopencv.com/getting-started-with-opencv/

Set up environment
- download open cv
- https://pypi.org/project/opencv-python/

Read, write, and display image
- cv_image.py
- https://learnopencv.com/read-display-and-write-an-image-using-opencv/
Resize image
- cv_resize.py
- https://learnopencv.com/image-resizing-with-opencv/
Adding text and shapes
- cv_draw1.py cv_draw2.py
- https://learnopencv.com/annotating-images-using-opencv/
Displaying video
- cv_video.py
- https://learnopencv.com/reading-and-writing-videos-using-opencv/

Saving and recording video
- manipulate video settings
    - https://www.geeksforgeeks.org/how-to-get-properties-of-python-cv2-videocapture-object/#
- save video
    - cv_video_save.py
    - https://learnopencv.com/reading-and-writing-videos-using-opencv/
'''



# Hello this is a one line comment

'''
This is a comment block
It stretches out over multiple lines
So that you dont need a '#' every time
'''

import cv2

# Get the video from the file
video = cv2.VideoCapture('bp.mp4') # Change the file name to 0 to read the webcam

frame_size = (int(video.get(3)), int(video.get(4)))
writer = cv2.VideoWriter('edit_bp.mp4', fourcc=cv2.VideoWriter_fourcc(*'XVID'), fps=20, frameSize=frame_size) # Start saving a video

if not video.isOpened():
    print("Error with video file...")

# Check if the video is open
while video.isOpened():

    # Read the next frame of the video
    success, frame = video.read()

    if success:
        cv2.circle(frame, (frame.shape[1]//2, frame.shape[0]//2), 100, (255,255,0), thickness=5)

        cv2.imshow("Video 1", frame)
        writer.write(frame) # Save frames to recording


        key = cv2.waitKey(100) #how much time between frames

        if key == ord('q'):
            break


    else:
        break

video.release()
writer.release() # Close the writer
cv2.destroyAllWindows()

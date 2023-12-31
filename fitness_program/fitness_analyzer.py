import Exercises.Pullup as Pullup
import Exercises.Pushup as Pushup
import Exercises.Squat as Squat
import Exercises.Plank as Plank
import Exercises.Situp as Situp
import Exercises.Jumpingjacks as Jumpingjacks
import Exercises.Muscleup as Muscleup
import Exercises.Lunge as Lunge
import Exercises.Sideplanks as Sideplanks
import Exercises.Kneeraises as Kneeraises

import firebase_manager
import cv2

# Connect to database
manager = firebase_manager.firebaseManager()

def fitnessAnalyzer(exercise, videoLocation, videoNameAnalyzed, upload=True, show=False):

    # Select what video to open up and access
    video = cv2.VideoCapture(videoLocation)

    # Create a writer to save the video
    VideoWidth = video.get(cv2.CAP_PROP_FRAME_WIDTH) 
    VideoHeight = video.get(cv2.CAP_PROP_FRAME_HEIGHT) 
    VideoFPS = video.get(cv2.CAP_PROP_FPS) 
    VideoSize = (int(VideoWidth), int(VideoHeight)) #tuple: used to group things
    videoFile = 'resources/' + videoNameAnalyzed + '.mp4'
    writer = cv2.VideoWriter(videoFile, fourcc=cv2.VideoWriter_fourcc('m','p','4','v'), fps=VideoFPS, frameSize=VideoSize) # Start saving a video

    # Select what exercise analyzer to use
    analyzer = None
    if exercise == 'Pushup':
        analyzer = Pushup.set()
        print("Running Pushup")
    if exercise == 'Pullup':
        analyzer = Pullup.set()
        print("Running Pullup")
    if exercise == 'Squat':
        analyzer = Squat.set()
        print('Running Squat')
    if exercise == 'Plank':
        analyzer = Plank.set(VideoFPS)
        print("Running Plank")
    if exercise == 'Sit Up':
        analyzer = Situp.set()
        print("Running Sit Up")
    if exercise == "Jumping Jacks":
        analyzer = Jumpingjacks.set()
        print("Running Jumping Jack")
    if exercise == "Muscle Up":
        analyzer = Muscleup.set()
        print("Running Muscle Up")
    if exercise == "Lunge":
        analyzer = Lunge.set()
        print("Running Lunge")
    if exercise == "Side Plank":
        analyzer = Sideplanks.set(VideoFPS)
        print("Running Side Planks")
    if exercise == "Knee Raise":
        analyzer = Kneeraises.set()
        print("Running Knee Raise")

    # Print error if video is not accessible
    if not video.isOpened():
        print("Error with video file...")

    # Check if the video is open
    while video.isOpened():

        # Read the next frame of the video
        success, frame = video.read()

        if success:

            # # If frame needs to be resized quickly
            # frame = cv2.resize(frame, (frame.shape[1]//3, frame.shape[0]//3))

            # Progess the rep based on the frame
            analyzer.process(frame)

            writer.write(frame) # Save frames to recording

            #shows video (DO NOT SEND TO SERVER)
            if show:
                cv2.imshow("Your Workout", frame)
                key = cv2.waitKey(0)
                if key == ord('q'):
                    break

        else:
            break

    video.release()
    writer.release()
    cv2.destroyAllWindows()
    
    if upload:
        LinkToVideo = manager.uploadFile(videoFile)
        return LinkToVideo
    
    return videoFile
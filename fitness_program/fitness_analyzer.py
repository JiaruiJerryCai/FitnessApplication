import Pullup
import Pushup
import Squat
import Plank
import firebase_manager
import cv2

manager = firebase_manager.firebaseManager()

def fitnessAnalyzer(exercise, videoLocation, videoNameAnalyzed):

    # Select what exercise analyzer to use
    analyzer = None
    if exercise == 'Pushup':
        analyzer = Pushup.set()
    if exercise == 'Pullup':
        analyzer = Pullup.set()

    # Select what video to open up and access
    video = cv2.VideoCapture(videoLocation)
    
    # Create a writer to save the video
    VideoWidth = video.get(cv2.CAP_PROP_FRAME_WIDTH) 
    VideoHeight = video.get(cv2.CAP_PROP_FRAME_HEIGHT) 
    VideoFPS = video.get(cv2.CAP_PROP_FPS) 
    VideoSize = (int(VideoWidth), int(VideoHeight)) #tuple: used to group things
    videoFile = 'resources/' + videoNameAnalyzed + '.mp4'
    writer = cv2.VideoWriter(videoFile, fourcc=cv2.VideoWriter_fourcc('m','p','4','v'), fps=VideoFPS, frameSize=VideoSize) # Start saving a video

    # Print error if video is not accessible
    if not video.isOpened():
        print("Error with video file...")

    # Check if the video is open
    while video.isOpened():

        # Read the next frame of the video
        success, frame = video.read()

        if success:
            # Progess the rep based on the frame
            analyzer.process(frame)

            cv2.imshow("Your Workout", frame)
            writer.write(frame) # Save frames to recording
            key = cv2.waitKey(20)
            if key == ord('q'):
                break

        else:
            break

    video.release()
    writer.release()
    LinkToVideo = manager.uploadFile(videoFile)
    cv2.destroyAllWindows()
    
    return LinkToVideo

        
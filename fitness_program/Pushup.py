import cv2
import mediapipe
import pose_detector

# create the body detector object
detector = pose_detector.Detector()

# Get the video from the file
video = cv2.VideoCapture('fitness_program/MyMovie.mp4') # Change the file name to 0 to read the webcam

if not video.isOpened():
    print("Error with video file...")

# Rep class used to track the completion and progress of a rep 
# and check if the rep had any errors
class rep:
    def __init__(self):
        # Variables to determine rep progress
        self.half_completed = None
        self.previous_location = None
        self.starting_position = None
        self.count = 0 
        self.correctCount = 0
        self.direction = None
        
        # Variables to determine if form is correct
        self.backAlwaysStraight = True
        self.armsFullyBent = False
        self.armFullyExtended = False
        self.kneeAlwaysStraight = True 

    def getDirection(self):
        return self.direction
    
    def getCount(self):
        return self.count
    
    def getCorrectCount(self):
        return self.correctCount

    def progress(self,angleofleftelbow,angleofleftbutt,angleofleftknee):

        # updateRep
        # checkForm

        # confirm rep finished
        
        # Calculate Direction
        if self.previous_location == None:
            _, self.previous_location = detector.getCoordinate(11) # left shoulder
        else:
            # Determine direction once the person has moved
            _, self.current_location = detector.getCoordinate(11)
            if self.previous_location > self.current_location:
                self.direction = "up" # up
            elif self.previous_location < self.current_location:
                self.direction = "down" #down
            self.previous_location = self.current_location
        # Figure out the starting position
        if self.direction != None:
            if self.direction == "up" and self.starting_position == None:
                self.starting_position = "bottom"
            elif self.direction == "down" and self.starting_position == None:
                self.starting_position = "top"
        
        # Check if one rep has been completed
        if self.starting_position != None:
            if self.starting_position == "top":
                if self.direction == "down" and self.half_completed:
                    self.half_completed = False
                    self.completed(angleofleftelbow,angleofleftbutt,angleofleftknee)
                if self.direction == "up":
                    self.half_completed = True
                
            if self.starting_position == "bottom":
                if self.direction == "up" and self.half_completed:
                    self.half_completed = False
                    self.completed(angleofleftelbow,angleofleftbutt,angleofleftknee)
                if self.direction == "down":
                    self.half_completed = True

    def completed(self,angleofleftelbow,angleofleftbutt,angleofleftknee):
        if self.checkForm(angleofleftelbow,angleofleftbutt,angleofleftknee):
            self.correctCount = self.correctCount + 1
        self.count = self.count + 1
        

        # Variables to determine if form is correct
        self.backAlwaysStraight = True
        self.armsFullyBent = False
        self.armFullyExtended = False
        self.kneeAlwaysStraight = True 


    def checkForm(self,angleofleftelbow,angleofleftbutt,angleofleftknee):
        # Verify if arms fully bent and extended during rep
        if self.getDirection() == "down": # the user is going down
            if angleofleftelbow < 70:
                self.armsFullyBent = True
        elif self.getDirection() == "up": # the user is going up
            if angleofleftelbow > 140:
                self.armFullyExtended = True
            
        # Verify the back is straight the entire rep
        if angleofleftbutt < 160 or angleofleftbutt > 190:
            self.backAlwaysStraight = False

        # Verify the knee was stright the entire rep
        if angleofleftknee < 145:
            self.kneeAlwaysStraight = False
            
        return self.armFullyExtended and self.armsFullyBent and self.backAlwaysStraight and self.kneeAlwaysStraight

pushupRep = rep()

# Check if the video is open
while video.isOpened():

    # Read the next frame of the video
    success, frame = video.read()

    if success:

        # Analyze the frame
        detector.analyze(frame)
        # Gather information about push up pose
        angleofleftelbow = detector.getAngle(15, 13, 11)
        angleofleftbutt = detector.getAngle(25, 23, 11)
        angleofleftknee = detector.getAngle(23, 25, 27)

        _, y = detector.getCoordinate(11)
        print(y)

        # Progess the rep based on the frame
        pushupRep.progress(angleofleftelbow,angleofleftbutt,angleofleftknee)
        print(pushupRep.starting_position)
        print(pushupRep.half_completed)

        # Annotate information to frame
        if pushupRep.getDirection() == "up":
            cv2.putText(frame, "up", (100,300), 16, 3, (0,0,255), thickness=5)
        elif pushupRep.getDirection() == "down":
            cv2.putText(frame, "down", (100,300), 16, 3, (0,0,255), thickness=5)
        cv2.putText(frame, str(pushupRep.getCorrectCount()), (100,500), 16, 3, (0,0,255), thickness=5)
        cv2.putText(frame, str(pushupRep.getCount()), (100,700), 16, 3, (0,0,255), thickness=5)

        cv2.imshow("Your Workout", frame)
        key = cv2.waitKey(0)
        if key == ord('q'):
            break

    else:
        break

video.release()
cv2.destroyAllWindows()

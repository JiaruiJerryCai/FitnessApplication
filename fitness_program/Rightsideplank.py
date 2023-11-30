import pose_detector
import cv2
import time

# Rep class used to track the completion and progress of a rep 
# and check if the rep had any errors
class set:
    def __init__(self, videoFPS):
        # Intialize the detector to recognize body parts from image
        self.detector = pose_detector.Detector()

        # Variables to determine rep progress
        self.starting_position = None
        self.frame = None
        self.videoFPS = videoFPS

        # Variables to determine if form is correct (everything should be true when correct)
        #Maintained body part
        self.backAlwaysStraight = True
        self.kneeAlwaysStraight = True
        self.headAlwaysStraight = True 
        self.rightArmAngleAlwaysWide = True
        self.leftArmAlwaysUp = True

        # Changing body part
        # ...
        
        # Error Dictionary
        self.error_dict = {}

    def getCount(self):
        return self.count

    def process(self, frame):

        # Use detector to analyze the frame
        self.detector.analyze(frame)
        
        try: 
            # Determine if posture is in plank formation
            if self.backAlwaysStraight and self.kneeAlwaysStraight and self.headAlwaysStraight and self.rightArmAngleAlwaysWide and self.leftArmAlwaysUp and self.frame == None:
                self.frame = 1

            # =========================== Check for Errors ========================
            backAngle = self.detector.getAngle(12,24,26) # Right shoulder, hip, knee
            kneeAngle = self.detector.getAngle(24,26,28) # Right hip, knee, ankle
            headAngle = self.detector.getAngle(8,12,24) # Right ear, shoulder, hip
            rightArmAngle = self.detector.getAngle(14,12,24) #Right elbow, shoulder, hip
            leftArmAngle = self.detector.getAngle(13,11,23) #Left elbow, shoulder, hip
                
            # Verify the back is straight
            error_msg = "back not straight"  
            if backAngle < 155 or backAngle > 190:
                self.backAlwaysStraight = False
                if error_msg not in self.error_dict:
                    self.error_dict[error_msg] = time.time()

            # Verify the knee is straight
            error_msg = "knee not straight"
            if kneeAngle < 145: 
                self.kneeAlwaysStraight = False
                if error_msg not in self.error_dict:
                    self.error_dict[error_msg] = time.time()

            # Verify if head is straight
            error_msg = "head not straight"
            if headAngle < 130: 
                self.headAlwaysStraight = False
                if error_msg not in self.error_dict:
                    self.error_dict[error_msg] = time.time()

            #Verify if left arm is wide enough
            error_msg = "right arm not wide enough"
            if rightArmAngle < 70: 
                self.rightArmAngleAlwaysWide = False
                if error_msg not in self.error_dict:
                    self.error_dict[error_msg] = time.time()

            #Verify if right arm is raised up
            error_msg = "left arm not raised"
            if leftArmAngle < 80: 
                self.leftArmAlwaysUp = False
                if error_msg not in self.error_dict:
                    self.error_dict[error_msg] = time.time()

            # =====================================================================

            self.completed()
            self.drawFeedback(frame)
        except:
            print("Error reading body")

    def completed(self):
        # Increase the timer
        if self.backAlwaysStraight and self.kneeAlwaysStraight and self.headAlwaysStraight and self.rightArmAngleAlwaysWide and self.leftArmAlwaysUp and self.frame:
            self.frame = self.frame + 1
        
        # Reset variables to determine if form is correct
        self.backAlwaysStraight = True
        self.kneeAlwaysStraight = True
        self.headAlwaysStraight = True 
        self.leftArmAngleAlwaysWide = True
        self.rightArmAlwaysUp = True


    def drawFeedback(self, frame):
        # Check error_dict to remove errors older than 2 seconds
        remove_list = []
        for error in self.error_dict:
            current_time = time.time()
            error_time = self.error_dict[error]
            if current_time - error_time > 2.0:
                remove_list.append(error)

        for error in remove_list:
            self.error_dict.pop(error)

        # Write the feedback onto the frame...
        # use self.error_dict to get all the errors you have
        x_origin = int(self.detector.image.shape[0]*0.2)
        y_origin = int(self.detector.image.shape[0]*0.2)
        row = 0
        spacing = int(self.detector.image.shape[0]*0.1)
        for error in self.error_dict:
            offset = row*spacing
            cv2.putText(frame, error, (x_origin,y_origin + offset), 16, 3, (0,0,255), thickness=5)
            row = row + 1

        # Draws the correct time in plank position
        if self.frame:
            timeInPosition = round(self.frame / self.videoFPS, 2)
            x_origin = int(self.detector.image.shape[0]*0.2)
            y_origin = int(self.detector.image.shape[0]*0.8)
            cv2.putText(frame, str(timeInPosition), (x_origin, y_origin), 16, 3, (0,0,255), thickness=5)

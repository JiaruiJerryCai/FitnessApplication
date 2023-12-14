import cv2
import pose_detector
import time

# Rep class used to track the completion and progress of a rep 
# and check if the rep had any errors
class set:
    def __init__(self):
        # Intialize the detector to recognize body parts from image
        self.detector = pose_detector.Detector()

        # Variables to determine rep progress
        self.half_completed = None
        self.previous_location = None
        self.count = 0 
        self.direction = None
        self.end_movement = None
        self.leftOrRight = None #left or right
        
        # Variables to determine if form is correct (everything should be true when correct)
        #Maintained body part
        self.backAlwaysStraight = True
        self.otherLegStraight = True

        #Changing body part
        self.legFullyBent = False
        self.legStraight = False

        
        # Error Dictionary
        self.error_dict = {}

    def getCount(self):
        return self.count

    def process(self, frame):

        # Use detector to analyze the frame
        self.detector.analyze(frame)
        
        try:
            # Calculate Direction
            if self.previous_location == None:
                _, self.previous_location = self.detector.getCoordinate(0) # nose
            else:
                # Determine direction once the person has moved
                _, self.current_location = self.detector.getCoordinate(0)
                if self.previous_location - (self.detector.getDistance(13,15) * 0.04) > self.current_location:
                    self.direction = "up" # up
                elif self.previous_location + (self.detector.getDistance(13,15) * 0.04) < self.current_location:
                    self.direction = "down" #down
                self.previous_location = self.current_location
            
            # Check if left or right leg is used
            right = self.detector.getDistance(0,26)
            left = self.detector.getDistance(0,25)
            if left > right:
                self.leftOrRight = "right"
            elif left < right: 
                self.leftOrRight = "left"


            if self.leftOrRight == "left":
                if self.direction != None:
                    leftlegangle = self.detector.getAngle(27,25,23)
                    righthipangle = self.detector.getAngle(12,24,26)
                    if leftlegangle < 100 and righthipangle > 160 and self.direction == "up":
                        self.legFullyBent = True
                        self.half_completed = True
                    if leftlegangle > 140 and righthipangle > 160:
                        self.legStraight = True
                        if self.half_completed:
                            self.completed()
                            self.end_movement = True

            if self.leftOrRight == "right":
                if self.direction != None:
                    rightlegangle = self.detector.getAngle(28,26,24)
                    lefthipangle = self.detector.getAngle(11,23,25)
                    if rightlegangle < 100 and lefthipangle > 160 and self.direction == "up":
                        self.legFullyBent = True
                        self.half_completed = True
                    if rightlegangle > 140 and lefthipangle > 160:
                        self.legStraight = True
                        if self.half_completed:
                            self.completed()
                            self.end_movement = True

            # Mark end of ending movement
            if self.end_movement and self.direction == "down":
                self.end_movement = False

            # =========================== Check for Errors ========================
                
            #Left leg
            

            # =====================================================================

            self.drawFeedback(frame)
        except:
            print("Error reading body")

    def completed(self):
        # Increase the count of reps
        if self.backAlwaysStraight and self.otherLegStraight and self.legFullyBent and self.legStraight:
            self.count = self.count + 1
        
        # Variables to determine if form is correct
        # Variables to determine rep progress
        self.half_completed = None
        self.leftOrRight = None #left or right
        
        # Variables to determine if form is correct (everything should be true when correct)
        #Maintained body part

        #Changing body part
        self.legFullyBent = False
        self.legStraight = False

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

        # Draws the amount of reps performed
        x_origin = int(self.detector.image.shape[0]*0.2)
        y_origin = int(self.detector.image.shape[0]*0.8)
        cv2.putText(frame, str(self.count), (x_origin, y_origin), 16, 3, (0,0,255), thickness=5)

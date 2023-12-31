import fitness_program.pose_detector as pose_detector
import time
import cv2

# Rep class used to track the completion and progress of a rep 
# and check if the rep had any errors
class set:
    def __init__(self):
        # Intialize the detector to recognize body parts from image
        self.detector = pose_detector.Detector()

        # Variables to determine rep progress
        self.bar = None
        self.previous_location = None
        self.current_location = None
        self.count = 0 
        self.direction = None
        self.directionCountDown = 0
        self.directionCountUp = 0
        self.end_movement = None
        
        # Variables to determine if form is correct (everything should be true when correct)
        # Maintained body part
        # Changing body part
        self.armsFullyExtendedBelowBar = False
        self.armsFullyExtendedAboveBar = False
        
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
                if self.previous_location + (self.detector.getDistance(13,15) * 0) > self.current_location:
                    self.direction = "up" 
                elif self.previous_location - (self.detector.getDistance(13,15) * 0) < self.current_location:
                    self.direction = "down" 
                self.previous_location = self.current_location

            # Figure out if we are below or above the bar.
            _, location_shoulder = self.detector.getCoordinate(11)
            _, location_hand = self.detector.getCoordinate(15)
            if location_shoulder < location_hand:
                self.bar = "above"
            else:
                self.bar = "below"
                
            # Check if one rep has been completed
            leftelbowangle = self.detector.getAngle(11,13,15)
            rightelbowangle = self.detector.getAngle(16,14,12)
            if self.direction != None:
                # if below bar and arms are straight
                if self.bar == "below" and leftelbowangle > 150 and rightelbowangle > 150 and self.direction == "up":
                    self.armsFullyExtendedBelowBar = True
                if self.bar == "above" and leftelbowangle > 150 and rightelbowangle > 150 and self.direction == "down":
                    self.armsFullyExtendedAboveBar = True
                if leftelbowangle > 160 and leftelbowangle < 190 and rightelbowangle > 160 and rightelbowangle < 190 and self.armsFullyExtendedAboveBar and self.armsFullyExtendedBelowBar and self.bar == "below":
                    self.completed()
                    self.end_movement = True

            # Mark end of ending movement
            if self.end_movement and self.bar == "below":
                self.end_movement = False

            # =========================== Check for Errors ========================

            # Error: Reached top of bar, but failed to straighten arms above the bar
            error_msg = "above the bar"
            if self.bar == "above" and self.armsFullyExtendedAboveBar == False:
                if self.direction == "down":
                    self.directionCountDown = self.directionCountDown + 1
                    if self.directionCountDown == 5:
                        if error_msg not in self.error_dict:
                            self.error_dict[error_msg] = time.time()
                else:
                    self.directionCountDown = 0


            # Error: Failed to straighten arm below the bar (completing the movement) before starting the next rep
            error_msg = "below the bar"
            if self.bar == "below" and self.armsFullyExtendedBelowBar == False:
                if self.direction == "up":
                    self.directionCountUp = self.directionCountUp + 1
                    if self.directionCountUp == 5:
                        if error_msg not in self.error_dict:
                            self.error_dict[error_msg] = time.time()
                else:
                    self.directionCount = 0
            
            # =====================================================================

            self.drawFeedback(frame)
        except:
            print("Error reading body")


    def completed(self):
        print("hit completed")
        # Increase the count of reps
        if self.armsFullyExtendedAboveBar and self.armsFullyExtendedBelowBar:
            self.count = self.count + 1
        
        # Variables to determine if form is correct
        #Changing body part
        self.armsFullyExtendedAboveBar = False
        self.armsFullyExtendedBelowBar = False


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

        # cv2.putText(frame, str(self.direction), (x_origin + 100, y_origin + 0) , 16, 1, (0,0,255), thickness=2)
        # cv2.putText(frame, "Bar: " + str(self.bar), (x_origin + 100, y_origin + 50) , 16, 1, (0,0,255), thickness=2)
        # cv2.putText(frame, "Below Bar: " + str(self.armsFullyExtendedBelowBar), (x_origin + 100, y_origin + 100), 16, 1, (0,0,255), thickness=2)
        # cv2.putText(frame, "Above Bar: " + str(self.armsFullyExtendedAboveBar), (x_origin + 100, y_origin + 150), 16, 1, (0,0,255), thickness=2)

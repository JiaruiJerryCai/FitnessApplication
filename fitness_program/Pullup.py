#incomplete
import cv2
import mediapipe
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
        self.starting_position = None
        self.count = 0 
        self.direction = None
        self.end_movement = None
        
        # Variables to determine if form is correct (everything should be true when correct)
        # Maintained body part
        
        '''
        Take better consideration of what conditions you want to keep track of as the pullup progresses
        Also remember to initialize all your variables here
        '''

        self.armsAlwaysWide = True
        self.headAlwaysStraight = True
        # Changing body part
        self.noseAboveHand = False
        self.armsFullyBent = False
        self.armsFullyExtended = False
        
        # Error Dictionary
        self.error_dict = {}

    def getCount(self):
        return self.count

    def process(self, frame):

        # Use detector to analyze the frame
        self.detector.analyze(frame)

        # Calculate Direction
        if self.previous_location == None:
            _, self.previous_location = self.detector.getCoordinate(11) # left shoulder
        else:
            # Determine direction once the person has moved
            _, self.current_location = self.detector.getCoordinate(11)
            if self.previous_location + (self.detector.getDistance(13,15) * 0.07) > self.current_location:
                self.direction = "up" 
            elif self.previous_location - (self.detector.getDistance(13,15) * 0.07) < self.current_location:
                self.direction = "down" 
            self.previous_location = self.current_location
            

        print("Direction:", self.direction)
        # Check if one rep has been completed
        leftelbowangle = self.detector.getAngle(15,13,11)
        rightelbowangle = self.detector.getAngle(12,14,16)
        if self.direction != None:
            if leftelbowangle < 100 and rightelbowangle < 100 and self.direction == "up":
                self.armsFullyBent = True
                self.half_completed = True
            if leftelbowangle > 150 and rightelbowangle > 150:
                self.armsFullyExtended = True
                if self.half_completed:
                    self.completed()
                    self.end_movement = True

        # Mark end of ending movement
        if self.end_movement and self.direction == "up":
            self.end_movement = False

        # =========================== Check for Errors ========================

        # Verify the arms are wide the entire rep
        '''
        Arms should be measured via distance
        '''
        error_msg = "arms not wide enough"
        if leftelbowangle < 80 or leftelbowangle > 100 or rightelbowangle < 80 or rightelbowangle > 100: 
            self.armsAlwaysWide = False
            if error_msg not in self.error_dict:
                self.error_dict[error_msg] = time.time()

        # Verify the nose is above the hand
        error_msg = "head not high enough"
        _, location_nose = self.detector.getCoordinate(0)
        _, location_hand = self.detector.getCoordinate(15)
        if location_nose > location_hand and self.half_completed == False:
            if error_msg not in self.error_dict:
                self.error_dict[error_msg] = time.time()

        # Arms did not extend fully
        error_msg = "arms not extended"
        if not self.end_movement and self.direction == "down" and self.armsFullyBent == False:
            if error_msg not in self.error_dict:
                self.error_dict[error_msg] = time.time()

        # =====================================================================

        self.drawFeedback(frame)

    def completed(self):
        # Increase the count of reps
        if self.headAlwaysStraight and self.noseAboveArm and self.armsFullyBent and self.armsFullyExtended and self.armsAlwaysWide:
            self.count = self.count + 1
        
        # Variables to determine if form is correct
        self.armsAlwaysWide = True
        self.headAlwaysStraight = True 
        #Changing body part
        self.noseAboveArm = False
        self.armsFullyBent = False
        self.armsFullyExtended = False


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
        cv2.putText(frame, str(self.count), (100,700), 16, 3, (0,0,255), thickness=5)

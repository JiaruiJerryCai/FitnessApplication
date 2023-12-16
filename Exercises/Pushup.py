import cv2
import fitness_program.pose_detector as pose_detector
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
        #Maintained body part
        self.backAlwaysStraight = True
        self.kneeAlwaysStraight = True
        self.headAlwaysStraight = True 
        #Changing body part
        self.armsFullyBent = False
        self.armsFullyExtended = False
        
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
                _, self.previous_location = self.detector.getCoordinate(11) # left shoulder
            else:
                # Determine direction once the person has moved
                _, self.current_location = self.detector.getCoordinate(11)
                if self.previous_location - (self.detector.getDistance(13,15) * 0.04) > self.current_location:
                    self.direction = "up" # up
                elif self.previous_location + (self.detector.getDistance(13,15) * 0.04) < self.current_location:
                    self.direction = "down" #down
                self.previous_location = self.current_location
                
                
            # Check if one rep has been completed
            if self.direction != None:
                leftelbowangle = self.detector.getAngle(15,13,11)
                if leftelbowangle < 70 and self.direction == "down":
                    self.armsFullyBent = True
                    self.half_completed = True
                if leftelbowangle > 140:
                    self.armsFullyExtended = True
                    if self.half_completed:
                        self.completed()
                        self.end_movement = True

            # Mark end of ending movement
            if self.end_movement and self.direction == "down":
                self.end_movement = False

            # =========================== Check for Errors ========================
                
            # Verify the back is straight the entire rep
            error_msg = "back not straight"
            angleofleftbutt = self.detector.getAngle(25, 23, 11)
            if angleofleftbutt < 155 or angleofleftbutt > 190: 
                self.backAlwaysStraight = False
                if error_msg not in self.error_dict:
                    self.error_dict[error_msg] = time.time()

            # Verify the knee was stright the entire rep
            error_msg = "knee not straight"
            angleofleftknee = self.detector.getAngle(23, 25, 27)
            if angleofleftknee < 145: 
                self.kneeAlwaysStraight = False
                if error_msg not in self.error_dict:
                    self.error_dict[error_msg] = time.time()

            # Verify if arms were fully bent and chest was lowered for rep
            error_msg = "chest not low enough"
            if not self.end_movement and self.direction == "up" and self.armsFullyBent == False:
                if error_msg not in self.error_dict:
                    self.error_dict[error_msg] = time.time()

            # Verify if arms were fully extended and chest was raised for rep
            error_msg = "chest not high enough"
            if self.direction == "down" and self.armsFullyExtended == False:
                if error_msg not in self.error_dict:
                    self.error_dict[error_msg] = time.time()

            # Verify if head is straight with back for rep
            error_msg = "head not straight"
            if self.detector.getAngle(23,11,7) < 130: 
                self.headAlwaysStraight = False
                if error_msg not in self.error_dict:
                    self.error_dict[error_msg] = time.time()

            # =====================================================================

            self.drawFeedback(frame)
        except:
            print("Error reading body")

    def completed(self):
        # Increase the count of reps
        if self.backAlwaysStraight and self.kneeAlwaysStraight and self.headAlwaysStraight and self.armsFullyBent and self.armsFullyExtended:
            self.count = self.count + 1
        
        # Variables to determine if form is correct
        self.backAlwaysStraight = True
        self.kneeAlwaysStraight = True 
        self.headAlwaysStraight = True
        self.armsFullyBent = False
        self.armsFullyExtended = False
        
        self.half_completed = False

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

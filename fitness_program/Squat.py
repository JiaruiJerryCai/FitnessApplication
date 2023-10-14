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
        # self.half_completed = None
        # self.previous_location = None
        # self.starting_position = None
        # self.count = 0 
        # self.direction = None
        # self.end_movement = None
        
        # Variables to determine if form is correct (everything should be true when correct)
        # Maintained body part
        # ...

        # Changing body part
        # ...
        
        # Error Dictionary
        self.error_dict = {}

    def getCount(self):
        return self.count

    def process(self, frame):

        # Use detector to analyze the frame
        self.detector.analyze(frame)
        
        # Get angle example
        self.detector.getMidpoint(12, 11)
        # =========================== Check for Errors ========================
            

        # =====================================================================

        self.drawFeedback(frame)

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

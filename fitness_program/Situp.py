import pose_detector
import time
import cv2

# Rep class used to track the completion and progress of a rep 
# and check if the rep had any errors
class set:
    def __init__(self):
        # Intialize the detector to recognize body parts from image
        self.detector = pose_detector.Detector()

        # Variables to determine rep progress
        self.half_completed = None
        self.startingPosition = None
        self.count = 0 
        
        # Variables to determine if form is correct (everything should be true when correct)
        # Maintained body part
        self.legNotStretched = True
        self.handCloseToHead = True

        # Changing body part
        self.bodyNotBentEnough = False
        self.bodyNotStretchedEnough = False
        
        # Error Dictionary
        self.error_dict = {}

    def getCount(self):
        return self.count

    def process(self, frame):

        # Use detector to analyze the frame
        self.detector.analyze(frame)

        try: 
            hipAngle = self.detector.getAngle(11,23,25)

            # Check if user is in starting position
            self.isHandCloseToEar()
            if self.startingPosition == None and hipAngle > 110 and self.handCloseToHead:
                self.startingPosition = True
                
            # Check if one rep has been completed
            if self.startingPosition:
                if hipAngle < 50: 
                    self.half_completed = True
                if self.half_completed and hipAngle > 110:
                    self.completed()

            # =========================== Check for Errors ========================

            # Check if hand is close to ear
            error_msg = "Hand is too far from ear"
            if self.handCloseToHead == False:
                if error_msg not in self.error_dict:
                    self.error_dict[error_msg] = time.time()

            # Check if leg is stretched
            legAngle = self.detector.getAngle(23,25,27)
            error_msg = "Legs are stretched too far"
            if legAngle > 80:
                self.legNotStretched = False
                if error_msg not in self.error_dict:
                    self.error_dict[error_msg] = time.time()


            # Check if body is bent halfway


            # Check if body is stretched at the end


            # =====================================================================

            self.drawFeedback(frame)
        except:
            print("Error reading body")

    def completed(self):
        # Increase the count of reps
        if self.handCloseToHead and self.legNotStretched:
            self.count = self.count + 1
        
        # Variables to determine if form is correct
        # Changing body part
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

    # Helper function that returns true if the hands are at the ears
    def isHandCloseToEar(self):
        
        righthandProximityToEar = self.detector.getDistance(16,8)
        if righthandProximityToEar <= (self.detector.getDistance(15,21)):
            rightClose = True
        else: 
            rightClose = False

        lefthandProximityToEar = self.detector.getDistance(15,7)
        if lefthandProximityToEar <= (self.detector.getDistance(15,21)):
            leftClose = True
        else: 
            leftClose = False 

        self.handCloseToHead = rightClose and leftClose
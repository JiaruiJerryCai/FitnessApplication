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
        self.starting_position = None
        self.count = 0 
        self.direction = None
        self.end_movement = None
        self.pose = "close"  # "open" or "close" 
        self.reachedTop =  False
        self.reachedBottom = True
        
        # Variables to determine if form is correct (everything should be true when correct)
        #Maintained body part
        
        #Changing body part

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
                _, self.previous_location = self.detector.getCoordinate(0) # left shoulder
            else:
                # Determine direction once the person has moved
                _, self.current_location = self.detector.getCoordinate(0)
                if self.previous_location - (self.detector.getDistance(13,15) * 0.04) > self.current_location:
                    self.direction = "up" # up
                elif self.previous_location + (self.detector.getDistance(13,15) * 0.04) < self.current_location:
                    self.direction = "down" #down
                self.previous_location = self.current_location
                
                
            # Check if one half of the jumping jack has been completed
            if self.direction != None:

                # Count one jump
                if self.direction == "down":
                    self.reachedTop = True
                if self.direction == "up" and self.reachedTop:
                    self.completed()


            # Mark end of ending movement
            if self.end_movement and self.direction == "down":
                self.end_movement = False

            # =========================== Check for Errors ========================

            armAngle = self.detector.getAngle(13,11,23)
            if self.pose == "open":
                # Errors for open pose
                # Verify if the arm is raised high enough
                error_msg = "Arms not raised high enough"
                if armAngle < 100  and self.direction == "down":
                    if error_msg not in self.error_dict:
                        self.error_dict[error_msg] = time.time()
            

            if self.pose == "close":
                # Errors for close pose
                error_msg = "Arms not closed"
                if armAngle > 10  and self.direction == "up":
                    if error_msg not in self.error_dict:
                        self.error_dict[error_msg] = time.time()

            # =====================================================================

            self.drawFeedback(frame)
        except:
            print("Error reading body")

    def completed(self):
        # Increase the count of reps
        self.count = self.count + 0.5

        if self.pose == "open":
            self.pose = "close"
        elif self.pose == "close":
            self.pose = "open"
        
        # Variables to determine if form is correct
        self.reachedTop = False


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

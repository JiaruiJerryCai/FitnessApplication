import mediapipe
import math
import cv2

class Detector:
    # Constructor
    # Defines what information the object stores
    def __init__(self):
        self.mp_drawing = mediapipe.solutions.drawing_utils
        self.mp_pose = mediapipe.solutions.pose
        self.pose = self.mp_pose.Pose()
        self.results = None

    # Used to fill the results of the object
    def analyze(self,image):
        # Convert image from BGR to RGB for mediapipe to read with better accuracy
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(rgb)
        
        # Draw points on top of image
        self.mp_drawing.draw_landmarks(image, self.results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)

    
    # Get results
    def getResults(self):
        return self.results
    
    # Gives the coordinates of specific body parts
    def getCoordinate(self,body_part):
        return self.results.pose_landmarks.landmark[body_part]
    
    # Retrieves slope between two selected body parts
    def getSlope(self, body_part1, body_part2):
        bp1x = self.results.pose_landmarks.landmark[body_part1].x
        bp1y = self.results.pose_landmarks.landmark[body_part1].y
        bp2x = self.results.pose_landmarks.landmark[body_part2].x
        bp2y = self.results.pose_landmarks.landmark[body_part2].y

        # Calculate slope
        slope = (bp2y - bp1y) / (bp2x - bp1x)
        
        return slope
    
    # Retrieves distance between two selected body parts
    def getDistance(self, body_part1, body_part2): 
        bp1x = self.results.pose_landmarks.landmark[body_part1].x
        bp1y = self.results.pose_landmarks.landmark[body_part1].y
        bp2x = self.results.pose_landmarks.landmark[body_part2].x
        bp2y = self.results.pose_landmarks.landmark[body_part2].y

        # Calculate distance
        distance = math.sqrt((bp2y - bp1y)**2 + (bp2x - bp1x)**2)

        return distance
    
    # Retrieves angle between three selected body parts
    def getAngle(self, body_part1, body_part2, body_part3):
        bp1x = self.results.pose_landmarks.landmark[body_part1].x
        bp1y = self.results.pose_landmarks.landmark[body_part1].y
        bp2x = self.results.pose_landmarks.landmark[body_part2].x
        bp2y = self.results.pose_landmarks.landmark[body_part2].y
        bp3x = self.results.pose_landmarks.landmark[body_part3].x
        bp3y = self.results.pose_landmarks.landmark[body_part3].y

        # Calculates angle of joint from 3 points
        angle = math.atan2(bp3y - bp1y, bp3x - bp1x) - math.atan2(bp2y - bp1y, bp2x - bp1x)
        angle_degrees = angle * (180/math.pi)

        return angle_degrees
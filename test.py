import pyttsx3
import math
import cv2
import mediapipe as mp
import time

# Important functions to be used in pose detection
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

# For webcam input:


def pose():
  cap = cv2.VideoCapture(0)
  with mp_pose.Pose(
          min_detection_confidence=0.5,
          min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
      success, image = cap.read()
      if not success:
        print("Ignoring empty camera frame.")
        # If loading a video, use 'break' instead of 'continue'.
        continue

      # Flip the image horizontally for a later selfie-view display, and convert
      # the BGR image to RGB.
      image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
      # To improve performance, optionally mark the image as not writeable to
      # pass by reference.
      image.flags.writeable = False
      results = pose.process(image)

      # Draw the pose annotation on the image.
      image.flags.writeable = True
      image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
      mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

      # mp_drawing.plot_landmarks(results.pose_world_landmarks, mp_pose.POSE_CONNECTIONS)

      #convert the landmarks JSON to a list of dictionary
      keypoints = [{'X': data.x, 'Y': data.y, 'Z': data.z}
                   for data in results.pose_landmarks.landmark]

      #convert the local variables to global ones
      global arc1
      arc1 = keypoints[9]   # soulder arc
      global arc2
      arc2 = keypoints[22]  # right arc
      global arc3
      arc3 = keypoints[23]  # left arc
      global arc4
      arc4 = keypoints[24]  # hip arc

      #To calculate the distance
      distance = 0
      distance += ((arc1['X']) - (arc4['X']))**2
      distance += ((arc1['Y']) - (arc4['Y']))**2
      distance += ((arc1['Z']) - (arc4['Z']))**2
      result = math.sqrt(distance)
      if result < 0.7*0.9829993072752983:
        engine = pyttsx3.init()
        engine.say('Sit straight you moron')
        engine.runAndWait()
      # print(result)
      cv2.imshow('MediaPipe Pose', image)
      if cv2.waitKey(10) & 0xFF == ord('q'):
        break
  cap.release()

  # print(keypoints)
pose()

# def calculatedistance(c1, c4):
#   #To calculate the distanceance
#   distance = 0
#   distance += ((c1['X']) - (c4['X']))**2
#   distance += ((c1['Y']) - (c4['Y']))**2
#   distance += ((c1['Z']) - (c4['Z']))**2
#   result = math.sqrt(distance)
#   if result < 0.8*0.9665996894753616:
#       engine = pyttsx3.init()
#       # time.sleep(5)
#       engine.say('Sit straight you moron')
#       engine.runAndWait()
#   print(result)
# calculatedistanceance(arc1,arc4)

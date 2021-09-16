import pyttsx3
from dotenv import load_dotenv
import math
import cv2
import mediapipe as mp

# Important functions to be used in pose detection
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose


# def CalculateTime(t):

# 	while t:
# 		mins, secs = divmod(t, 60)
# 		timer = '{:02d}:{:02d}'.format(mins, secs)
# 		print(timer, end="\r")
# 		time.sleep(1)
# 		t -= 1

# 	print('Fire in the hole!!')

# if sec%5==0: var = q else var = B

# For webcam input:
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
    mp_drawing.draw_landmarks(image,results.pose_landmarks,mp_pose.POSE_CONNECTIONS,landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

    # mp_drawing.plot_landmarks(results.pose_world_landmarks, mp_pose.POSE_CONNECTIONS)

    keypoints = [{'X': data.x, 'Y': data.y, 'Z': data.z} for data in results.pose_landmarks.landmark]

    cv2.imshow('MediaPipe Pose', image)
    if cv2.waitKey(5) & 0xFF == ord('q'):
      break
cap.release()
# To calculate the distance

for i in range(len(keypoints)):
    # print(f'{i}\n {keypoints[i]}\n\n')
    arc1 = keypoints[9]  # soulder arc
    arc2 = keypoints[22]  # right arc
    arc3 = keypoints[23]  # left arc
    arc4 = keypoints[24]  # hip arc


def calculateDistance(C1, C2):
    dist = 0
    dist += ((C1['X']) - (C2['X']))**2
    dist += ((C1['Y']) - (C2['Y']))**2
    dist += ((C1['Z']) - (C2['Z']))**2
    result = math.sqrt(dist)
    return result
distance = calculateDistance(arc1, arc4)

if distance < 1:
    engine = pyttsx3.init()
    engine.say('Sit straight you moron')
    engine.runAndWait()



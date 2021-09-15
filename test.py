import math
import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_holistic = mp.solutions.holistic
keypoints=[]

# For webcam input:
cap = cv2.VideoCapture(0)
with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
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
    results = holistic.process(image)

    # Draw landmark annotation on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

    # mp_drawing.plot_landmarks(results.pose_world_landmarks, mp_holistic.POSE_CONNECTIONS)

    

    cv2.imshow('MediaPipe Holistic', image)
    if cv2.waitKey(5) & 0xFF == ord('q'):
      break
    
for data in results.pose_landmarks.landmark:
  keypoints.append({'X': data.x,
                    'Y': data.y,
                    'Z': data.z,
                    
                    # 'Visibility': data.visibility,
                    })

for i in range(len(keypoints)):
  print(f'{i}\n {keypoints[i]}\n\n')

a = keypoints[9]  # soulder arc
b = keypoints[22] # right arc
c = keypoints[23] # left arc
d = keypoints[24] # hip arc


# print(results.pose_landmarks)

def calculate(C1, C2):
        dist = 0
        dist += ((C1['X']) - (C2['X']))**2
        dist += ((C1['Y']) - (C2['Y']))**2
        dist += ((C1['Z']) - (C2['Z']))**2
        result = math.sqrt(dist)
        print(result)

print(f'distance : {calculate(a,d)} ')

cap.release()


#  for - i (0 -> 10)
#   each : 5 sec me "Q" 
# 
# 
# 
# 
# 
#  

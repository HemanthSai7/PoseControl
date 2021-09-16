import azure.cognitiveservices.speech as speech_sdk
import os
from dotenv import load_dotenv
import math
import cv2
import mediapipe as mp

# Important functions to be used in pose detection
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_holistic = mp.solutions.holistic


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

        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
                                  landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

        # mp_drawing.plot_landmarks(results.pose_world_landmarks, mp_holistic.POSE_CONNECTIONS)

        keypoints = [{'X': data.x, 'Y': data.y, 'Z': data.z}
                     for data in results.pose_landmarks.landmark]

        cv2.imshow('MediaPipe Holistic', image)
        if cv2.waitKey(10) & 0xFF == ord('q'):
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
    print(result)

# Azure text to speech


def main():
    try:
        global speech_config
        global translation_config

        # Get Configuration Setttings
        load_dotenv()
        cog_key = os.getenv('COG_SERVICE_KEY')
        cog_region = os.getenv('COG_sERVICE_REGION')

        # Configure speech service
        speech_config = speech_sdk.SpeechConfig(cog_key, cog_region)
        print('Ready to use speech service in:', speech_config.region)

    except Exception as ex:
        print(ex)


def TellWarning():
    if calculateDistance(arc1, arc4) < 0.7*0.9665996894753616:
        response_text = 'Sit straight you moron'

    # Configure speech synthesis
    speech_synthesizer = speech_sdk.SpeechSynthesizer(speech_config)
    speech_config.speech_synthesis_voice_name = 'en-GB-george'
    speech_synthesizer = speech_sdk.SpeechSynthesizer(speech_config)

    # Synthesize spoken output
    responseSsml = f"\
        <speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='en-US'> \
            <voice name='en-GB-Susan'> \
                {response_text} \
                    <break strength='weak'/> \
                        </voice> \
        </speak>"
    speak = speech_synthesizer.speak_ssml_async(response_text).get()
    if speak.reason != speech_sdk.ResultReason.SynthesizingAudioCompleted:
        print(speak.reason)

    # Print the response
    print(response_text)


if __name__ == '__main__':
    main()

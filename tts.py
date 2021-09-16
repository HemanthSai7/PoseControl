from dotenv import load_dotenv
import os
import azure.cognitiveservices.speech as speech_sdk

def main():
    try:
        global speech_config
        global translation_config

        #Get Configuration Setttings
        load_dotenv()
        cog_key=os.getenv('COG_SERVICE_KEY')
        cog_region=os.getenv('COG_sERVICE_REGION')

        #Configure speech service
        speech_config=speech_sdk.SpeechConfig(cog_key,cog_region)
        print('Ready to use speech service in:',speech_config.region)

    except Exception as ex:
        print(ex)    

def TellWarning():
    response_text=f'Sit straight you moron'

    #Configure speech synthesis
    speech_synthesizer=speech_sdk.SpeechSynthesizer(speech_config)
    speech_config.speech_synthesis_voice_name='en-GB-george'
    speech_synthesizer=speech_sdk.SpeechSynthesizer(speech_config)

    #Synthesize spoken output
    responseSsml = f"\
        <speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='en-US'> \
            <voice name='en-GB-Susan'> \
                {response_text} \
                    <break strength='weak'/> \
                        </voice> \
        </speak>"
    speak=speech_synthesizer.speak_ssml_async(response_text).get()
    if speak.reason!=speech_sdk.ResultReason.SynthesizingAudioCompleted:
        print(speak.reason)

    #Print the response
    print(response_text)

if __name__=='__main__':
    main()        



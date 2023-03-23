import requests

import azure.cognitiveservices.speech as speechsdk
from pydub import AudioSegment
import os
import uuid

import ConfigUtils

TTS_URL = "https://{0}.tts.speech.microsoft.com/cognitiveservices/v1"
AUDIO_OUTPUT_FORMAT = "audio-24khz-48kbitrate-mono-mp3"

# 合成语音并保存到本地
def text_to_speech(text, output_file):
    headers = {
        "Authorization": "Bearer " + get_access_token(),
        "Content-Type": "application/ssml+xml",
        "X-Microsoft-OutputFormat": AUDIO_OUTPUT_FORMAT,
        "User-Agent": "Mozilla/5.0"
    }

    VOICE_STYLE = ConfigUtils.getTTSConfig('voice_style')
    VOICE_NAME = ConfigUtils.getTTSConfig('voice_name')
    SPEAKING_RATE = ConfigUtils.getTTSConfig('speak_rate')
    LANG = ConfigUtils.getTTSConfig('lang')

    body = "<speak version='1.0' xmlns='https://www.w3.org/2001/10/synthesis' xmlns:mstts='https://www.w3.org/2001/mstts' xml:lang='{0}'>" \
        "<voice name='{1}'><prosody rate='{2}'><mstts:express-as role='Girl' style='{3}'>{4}</mstts:express-as></prosody></voice></speak>".format(
            LANG, VOICE_NAME, SPEAKING_RATE, VOICE_STYLE, text)
    
    response = requests.post(TTS_URL.format(
        ConfigUtils.getApiConfig('azure_region')), headers=headers, data=body.encode('utf-8'))
    if response.status_code == 200:
        with open(output_file, 'wb') as f:
            f.write(response.content)
    else:
        print("Failed to generate TTS audio file: {}".format(response.text))

# 获取 Azure 认知服务的访问令牌


def get_access_token():
    url = "https://{0}.api.cognitive.microsoft.com/sts/v1.0/issueToken".format(ConfigUtils.getApiConfig('azure_region'))
    headers = {
        "Ocp-Apim-Subscription-Key": ConfigUtils.getApiConfig('azure_api_key'),
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        print("Failed to get access token: {}".format(response.text))
        return None

def speech_to_text_url(file_path):
    url = 'https://westus.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1'#?language=en-US
    headers = {
        'Authorization': 'Bearer ' + get_access_token(),
        'Content-Type': 'audio/wav; codec="audio/pcm"; samplerate=16000'
    }
    # 打开 FLAC 文件
    flac_audio = AudioSegment.from_file(file=file_path, format="flac")

    # 将音频转换为 WAV 格式
    flac_audio.export(f"{file_path}.wav", format="wav")

    data = open(f"{file_path}.wav", 'rb').read()
    response = requests.post(url, data=data, headers=headers)

    print(response)

    if response.reason == speechsdk.ResultReason.RecognizedSpeech:
        responsestr = response.text
    else:
        responsestr = 'No speech could be recognize'

    os.remove(f"{file_path}.wav")

    return responsestr

def speech_to_text(file_path):

    config_subscription=ConfigUtils.getApiConfig('azure_api_key')
    config_region=ConfigUtils.getApiConfig('azure_region')
    config_speech_recognition_language=ConfigUtils.getTTSConfig('lang')

    if config_speech_recognition_language != 'en_US':
        speech_config = speechsdk.SpeechConfig(subscription=config_subscription,
                                            region=config_region,
                                            speech_recognition_language=config_speech_recognition_language)
    else:
        speech_config = speechsdk.SpeechConfig(subscription=config_subscription, region=config_region)
    # 打开 FLAC 文件
    flac_audio = AudioSegment.from_file(file=file_path, format="flac")


    file_id = str(uuid.uuid4())

    # 将音频转换为 WAV 格式
    flac_audio.export(f"{file_id}.wav", format="wav")

    audio_input = speechsdk.audio.AudioConfig(filename=f"{file_id}.wav")
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)

    result = speech_recognizer.recognize_once()

    # print(result)

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        responsestr = result.text
    else:
        responsestr = 'No speech could be recognize'

    # os.remove(f"{file_id}.wav")

    return responsestr


# 示例调用
if __name__ == '__main__':
    text = "参观了该市的一些设施"
    # text = "Haha, I promise I'm not an evil robot planning on taking over the world. What's up guy, do you love me?"
    output_file = "output.mp3"
    text_to_speech(text, output_file)

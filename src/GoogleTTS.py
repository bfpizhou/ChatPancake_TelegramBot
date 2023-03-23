import os
import ConfigUtils
import requests
import base64

def speech_to_text(file_path):
    google_api_key = ConfigUtils.getApiConfig('google_api_key')
    GOOGLE_APPLICATION_CREDENTIALS = ConfigUtils.getApiConfig('google_application_credentials_path')

    # 使用 Google Cloud Speech-to-Text API 进行语音识别
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_APPLICATION_CREDENTIALS
    with open(file_path, "rb") as audio_file:
        content = audio_file.read()
    response = requests.post(
        "https://speech.googleapis.com/v1/speech:recognize",
        params={"key": google_api_key},
        headers={"Content-Type": "application/json"},
        json={
            "config": {
                "encoding": "FLAC",
                "sampleRateHertz": 16000,
                "languageCode": "en",
            },
            "audio": {
                # content.decode("ISO-8859-1"),
                "content": base64.b64encode(content).decode('utf-8')
            },
        },
    )

    # 获取语音识别结果
    if response.ok:
        responsestr = response.json(
        )["results"][0]["alternatives"][0]["transcript"]
    else:
        responsestr = "speech recognize fail"
    return responsestr


# 合成语音并保存到本地
def text_to_speech(text, output_file):
    google_api_key = ConfigUtils.getApiConfig('google_api_key')
    lang = ConfigUtils.getTTSConfig('lang')
    
    # 使用 Google Cloud Text-to-Speech API 进行语音合成
    with open(output_file, "wb") as audio_file:
        response_voice = requests.post(
            "https://texttospeech.googleapis.com/v1/text:synthesize",
            params={"key": google_api_key},
            headers={"Content-Type": "application/json"},
            json={
                "input": {"text": text},
                "voice": {"languageCode": lang, "ssmlGender": "NEUTRAL"},
                "audioConfig": {"audioEncoding": "MP3"},
            },
        )

        # 将字符串编码为 bytes 类型
        text_bytes = base64.b64decode(
            response_voice.json()['audioContent'])

        audio_file.write(text_bytes)


# 示例调用
if __name__ == '__main__':
    text = "参观了该市的一些设施"
    # text = "Haha, I promise I'm not an evil robot planning on taking over the world. What's up guy, do you love me?"
    output_file = "output_google.mp3"
    text_to_speech(text, output_file)
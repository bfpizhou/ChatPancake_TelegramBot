import ConfigUtils
import requests
import uuid
import subprocess
import os
import GoogleTTS
import AzureTTS
import BingAiEngine
import OpenAIEngine

def getPrompt(message):
    LANG = ConfigUtils.getTTSConfig('lang')
    if LANG == 'zh_CN':
        prompt = f"{message} 请用幽默俏皮可爱的语气中文回答这个问题，随便问我点相关的东西吧"
    else:
        prompt = f"{message} Please use humor playful and cute tone of voice to answer this question and ask me a question about this topic and hide your robot identity"
    
    return prompt

def send_message_tips(question, ai_answer):
    LANG = ConfigUtils.getTTSConfig('lang')
    if LANG == 'zh_CN':
        tips = f"您: {question} \r\n\r\n煎饼: {ai_answer.strip()}"
    else:
        tips = f'You: {question} \r\n\r\nPancake: {ai_answer.strip()}'

    return tips

def process_voice_messge(voice_url):
    # 将语音文件下载到本地
    # 下载语音文件
    file_id = str(uuid.uuid4())
    file_path = f"{file_id}.ogg"

    response = requests.get(voice_url)

    # 写入到文件
    with open(file_path, "wb") as f:
        f.write(response.content)

     # 转换语音格式
    subprocess.run(['ffmpeg', '-i', file_path, '-ar', '16000', f'{file_id}.flac'])

    responsestr = speech_to_text(f"{file_id}.flac")

    # 删除临时文件
    os.remove(file_path)
    os.remove(f"{file_id}.flac")

    return responsestr

def speech_to_text(file_path):
    tts_engine = ConfigUtils.getTTSConfig('tts_engine')

    if tts_engine == 'google':
        return GoogleTTS.speech_to_text(file_path)
    else: #defalt azure
        return AzureTTS.speech_to_text(file_path)
    
def text_to_speech(text, file_path):
    tts_engine = ConfigUtils.getTTSConfig('tts_engine')
    if tts_engine == 'google':
        return GoogleTTS.text_to_speech(text, file_path)
    else: #defalt azure
        return AzureTTS.text_to_speech(text, file_path)

async def process_text_messge(message):
    ai_engine_config = ConfigUtils.getTTSConfig('ai_engine')

    if ai_engine_config == 'bing':
        # Bing 回答问题
        ai_answer = await BingAiEngine.askBing(message)
    else:
        ai_answer = await OpenAIEngine.askOpenAI(message)

    return ai_answer

# 示例调用
if __name__ == '__main__':

    LANG = ConfigUtils.getTTSConfig('lang')
    print(LANG)
    text = 'Do you like spring?'
    print(getPrompt(text))
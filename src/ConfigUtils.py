import json

CONFIG_FILE = 'config/config_api_key.json'
CONFIG_TTS_FILE = 'config/config_en_US.json' # config_zh_CN

def getApiConfig(config_name):
    with open(CONFIG_FILE) as f:
        data = json.load(f)
    
    try:
        config_value =  data['api_config'][config_name]
    except Exception as e:
        raise Exception(f"Read {config_name} of ApiConfig error",) from e
    
    return config_value

def getTTSConfig(config_name):
    with open(CONFIG_TTS_FILE) as f:
        data = json.load(f)
    
    try:
        config_value =  data['bot_tts_config'][config_name]
    except Exception as e:
        raise Exception(f"Read {config_name} of TTSConfig error",) from e
    
    return config_value


# 语音合成参数配置
# https://learn.microsoft.com/zh-cn/azure/cognitive-services/speech-service/language-support?tabs=tts
# https://learn.microsoft.com/zh-cn/azure/cognitive-services/speech-service/speech-synthesis-markup-voice
# en-US-ElizabethNeural en-US-JennyNeural  en-GB-MiaNeural zh-CN-XiaomoNeural en-US-AnaNeural zh-CN-XiaoshuangNeural
# VOICE_NAME = "en-US-JennyNeural"
# VOICE_STYLE = 'affectionate'
# SPEAKING_RATE = "0%"
# AUDIO_OUTPUT_FORMAT = "audio-24khz-48kbitrate-mono-mp3"
# # zh-CN-liaoning-XiaobeiNeural zh-CN-XiaomoNeural zh-TW-HsiaoYuNeural
# CHINESE_VOICE_NAME = "zh-CN-liaoning-XiaobeiNeural"

if __name__ == '__main__':
    # config_value = getApiConfig('telegram_bot_token')
    config_value = getTTSConfig('name')
    print(config_value)
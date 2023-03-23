import telebot
import os
import uuid
import mutagen.mp3
import asyncio
import emoji
import ChatEngine
import ConfigUtils

print('Start ChatTelegramBot...')
# 创建 Telegram Bot 对象
bot = telebot.TeleBot(ConfigUtils.getApiConfig('telegram_bot_token'))

def send_to_telegram_voice(message, question, ai_answer):

    file_id = str(uuid.uuid4())
    
    bot.send_message(message.chat.id, ChatEngine.send_message_tips(question, ai_answer))

    bot.send_chat_action(chat_id=message.chat.id, action='record_voice') #record_voice

    # 替换掉emoji方便转换语音
    ai_answer_for_tts = emoji.replace_emoji(ai_answer, '')
    ChatEngine.text_to_speech(ai_answer_for_tts, f"{file_id}.mp3")

    # 读取mp3文件
    with open(f"{file_id}.mp3", 'rb') as f:
        audio_read = f.read()

    # 打开音频文件
    audio = mutagen.mp3.MP3(f"{file_id}.mp3")

    # 获取音频长度
    voice_duration = audio.info.length

    # 发送语音回复
    bot.send_voice(chat_id=message.chat.id,
                voice=audio_read, duration=voice_duration)

    # 删除临时文件
    os.remove(f"{file_id}.mp3")

@bot.message_handler(content_types=['text'])
def handle_text(message):

    bot.send_chat_action(chat_id=message.chat.id, action='typing')
    ai_answer = asyncio.run(ChatEngine.process_text_messge(message.text))
    send_to_telegram_voice(message, message.text, ai_answer)

# 定义消息处理函数
@bot.message_handler(content_types=['voice'])
def handle_voice(message):
    voice_file = bot.get_file(message.voice.file_id)
    voice_url = f'https://api.telegram.org/file/bot{bot.token}/{voice_file.file_path}'
    responsestr = ChatEngine.process_voice_messge(voice_url)
    bot.send_chat_action(chat_id=message.chat.id, action='typing') 
    ai_answer = asyncio.run(ChatEngine.process_text_messge(responsestr))
    send_to_telegram_voice(message, responsestr, ai_answer)

# 开始轮询消息
bot.polling()

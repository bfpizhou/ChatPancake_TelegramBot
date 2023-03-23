import json
from EdgeGPT import Chatbot
import ChatEngine

# ConversationStyle  "creative", "balanced", "precise"
async def askBing(message, conversation_style='creative', isChinese = False):
    # bot = Chatbot()
    bot = Chatbot(cookiePath='cookie.json')
    response = await bot.ask(prompt=ChatEngine.getPrompt(message, isChinese), conversation_style=conversation_style)
    # response = await bot.ask(prompt=f"{message}", conversation_style=conversation_style)
    # print(answer)
    await bot.close()

    try:
        if 'text' in response['item']['messages'][1]:
            answer = response['item']['messages'][1]['text']
        elif 'text' in response["item"]["messages"][1]["adaptiveCards"][0]["body"][0]:
            answer = response["item"]["messages"][1]["adaptiveCards"][0]["body"][0]["text"]
        else:
            answer = response["item"]["messages"][1]["adaptiveCards"][0]["body"]['spokenText']

        # answer = response["item"]["messages"][1]["adaptiveCards"][0]["body"][0]["text"]
    except Exception as e:
        answer = response['item']['result']['message']
        # debugfile(response)

    # debugfile(answer)
    return clear_bing_answer(answer)


def clear_bing_answer(text):
    result = text.replace("[^1^]", "").replace("[^2^]", "").replace("[^3^]", "").replace("[^4^]", "").replace(
        "[^5^]", "").replace("[^6^]", "").replace("[^7^]", "").replace("[^8^]", "").replace("[^9^]", "").replace("[^10^]", "")
    return result


def debugfile(file_content):
    ttt = json.dumps(file_content).encode('utf-8')
    # 写入到文件
    with open('bing.json', "wb") as f:
        f.write(ttt)
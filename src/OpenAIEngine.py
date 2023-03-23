import openai
import asyncio
import json
import ChatEngine
import ConfigUtils

async def askOpenAI(question):
     # OPENAI 回答问题

    # 设置 OpenAI API 密钥
    openai.api_key = ConfigUtils.getApiConfig('openapi_key')

    # 定义上下文
    # context = "France is a beautiful country located in Western Europe. It is known for its rich history, culture, and cuisine. Paris is the capital city of France and is famous for its iconic landmarks such as the Eiffel Tower, the Louvre Museum, and the Notre-Dame Cathedral."

    # 调用 OpenAI GPT API 进行问题提问

    try:
        openai_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=[{"role": "user", "content": ChatEngine.getPrompt(question)}]
        )
        openai_answer = openai_response["choices"][0]["message"]['content']
    except Exception as e:
        openai_answer = e
    # openai_response = openai.Completion.create(
    #     engine="text-davinci-003", prompt=f"{question}",
    #     max_tokens=2000, n=1,stop=None,temperature=0.7
    # )
    # 输出回答
    # openai_answer = openai_response.choices[0].text.strip();

    return openai_answer

def debugfile(file_content):
    ttt = json.dumps(file_content).encode('utf-8')
    # 写入到文件
    with open('bing2.json', "wb") as f:
        f.write(ttt)

# 示例调用
if __name__ == '__main__':
    text = 'Do you like spring？'
    output_file = asyncio.run(askOpenAI(text))
    print(output_file)


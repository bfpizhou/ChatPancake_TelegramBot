> **Note**
> GPT-4 support will be added as soon as APIs are released to the public!

# ChatPancake Telegram Bot
![python-version](https://img.shields.io/badge/python-3.9-blue.svg)
[![openai-version](https://img.shields.io/badge/openai-0.27.2-orange.svg)](https://openai.com/)
[![license](https://img.shields.io/badge/License-GPL%202.0-brightgreen.svg)](LICENSE)

A [Telegram bot](https://core.telegram.org/bots/api) that integrates with OpenAI's _official_ [ChatGPT](https://openai.com/blog/chatgpt/) APIs to provide answers. Ready to use with minimal configuration required.

## Screenshots
![demo](https://github.com/bfpizhou/ChatPancake_TelegramBot/blob/main/Screenshots.png)

## Features
- [x] Humor chat bot

## Prerequisites
- Python 3.9+
- A [Telegram bot](https://core.telegram.org/bots#6-botfather) and its token (see [tutorial](https://core.telegram.org/bots/tutorial#obtain-your-bot-token))
- An [OpenAI](https://openai.com) account (see [configuration](#configuration) section)

## Getting started

### Configuration

About OpenAI Check out the [official API reference](https://platform.openai.com/docs/api-reference/chat) for more details.

About EdgeAI Check out the [Reverse engineered API of Microsoft's Bing Chat](https://github.com/acheong08/EdgeGPT) for more details.

### Installing
Clone the repository and navigate to the project directory:

```shell
git clone https://github.com/bfpizhou/ChatPancake_TelegramBot.git
cd ChatPancake_TelegramBot
```

#### From Source
1. Install the dependencies using `requirements.txt` file:
```shell
pip install -r requirements.txt
```
2. Setup the key in config/config_api_key.json

    About Google TTS Check out the [Google Text-to-Speech API](https://cloud.google.com/text-to-speech) for more details.

    About Azure TTS of MircoSoft Check out the [MircoSoft Text-to-Speech API](https://azure.microsoft.com/en-us/products/cognitive-services/text-to-speech/) for more details.

3. Setup bot language and accent in config folder

    Example:

    zh_CN => config_zh_CN.json
    en_US => config_en_US.json

    then update ConfigUtils.py for your config
    
4. Use the following command to start the bot:
```
python main.py
```

## Credits
- [ChatGPT](https://chat.openai.com/chat) from [OpenAI](https://openai.com)
- [python-telegram-bot](https://python-telegram-bot.org)
- [jiaaro/pydub](https://github.com/jiaaro/pydub)

## Disclaimer
This is a personal project and is not affiliated with OpenAI in any way.

## License
This project is released under the terms of the GPL 2.0 license. For more information, see the [LICENSE](LICENSE) file included in the repository.
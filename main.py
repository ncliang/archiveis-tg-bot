import os
import re
import urllib.parse

import flask
import functions_framework
import telegram


def is_valid_url(url: str) -> bool:
    try:
        result = urllib.parse.urlparse(url)
        if not all([result.scheme, result.netloc]):
            return False
        # Add additional checks for allowed schemes and domains
        allowed_schemes = {'http', 'https'}
        if result.scheme not in allowed_schemes:
            return False
        return True
    except Exception as e:
        # Log the specific error
        return False


def extract_urls(text: str) -> list[str]:
    # Regular expression to find URLs in text, excluding commas and URLs within angle brackets
    url_pattern = r'(?<!<)(?:https?://[^\s<>",]+|www\.[^\s<>",]+)(?!>)'
    urls = re.findall(url_pattern, text)
    return urls


def handle_message(bot, chat_id, message_text):
    # Extract all URLs from the message
    urls = extract_urls(message_text)
    for url in urls:
        if is_valid_url(url):
            encoded_url = urllib.parse.quote(url, safe=':/?=&')
            bot.sendMessage(chat_id=chat_id, text="https://archive.is/" + encoded_url)


@functions_framework.http
def telegram_webhook(request: flask.Request) -> flask.typing.ResponseReturnValue:
    bot = telegram.Bot(token=os.environ["ARCHIVE_BOT_TOKEN"])
    if request.method == "POST":
        try:
            update = telegram.Update.de_json(request.get_json(force=True), bot)
            if not update or not update.message:
                return "Invalid request format", 400
            chat_id = update.message.chat.id
            message_text = update.message.text

            handle_message(bot, chat_id, message_text)

        except Exception as e:
            # Log the error
            return "Error processing request", 500
    return "ok"

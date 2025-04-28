import os
import urllib.parse

import flask
import functions_framework
import telegram

def is_valid_url(url: str) -> bool:
    try:
        result = urllib.parse.urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

@functions_framework.http
def telegram_webhook(request: flask.Request) -> flask.typing.ResponseReturnValue:
    bot = telegram.Bot(token=os.environ["ARCHIVE_BOT_TOKEN"])
    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        chat_id = update.message.chat.id
        message_text = update.message.text
        
        if is_valid_url(message_text):
            bot.sendMessage(chat_id=chat_id, text="https://archive.is/" +message_text)
    return "ok"

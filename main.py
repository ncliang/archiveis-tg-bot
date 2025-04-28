import os
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

            if is_valid_url(message_text):
                message_text = urllib.parse.quote(message_text, safe=':/?=&')
                bot.sendMessage(chat_id=chat_id, text="https://archive.is/" +message_text)
        except Exception as e:
            # Log the error
            return "Error processing request", 500
    return "ok"

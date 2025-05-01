import json
import os
import re
import urllib.parse

import flask
import functions_framework
import telegram


def log(level: str, msg: str, **kwargs):
    """Log a message with the specified level and additional structured data.

    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR)
        msg: The message to log
        **kwargs: Additional structured data to include in the log
    """
    log_data = {
        'severity': level,
        'message': msg,
    }
    if kwargs:
        log_data.update(kwargs)

    print(json.dumps(log_data, ensure_ascii=False))


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
        log('ERROR', 'Error validating URL', url=url, error=str(e))
        return False


def extract_urls(text: str) -> list[str]:
    # Regular expression to find URLs in text, excluding commas and URLs within angle brackets
    url_pattern = r'(?<!<)(?:https?://[^\s<>",]+|www\.[^\s<>",]+)(?!>)'
    urls = re.findall(url_pattern, text)
    return urls


def handle_message(bot: telegram.Bot, chat_id: int, message_text: str) -> None:
    # Extract all URLs from the message
    urls = extract_urls(message_text)
    log('INFO', 'Processing message', chat_id=chat_id, url_count=len(urls))

    for url in urls:
        if is_valid_url(url):
            encoded_url = urllib.parse.quote(url, safe=':/?=&')
            archive_url = "https://archive.is/" + encoded_url
            bot.sendMessage(chat_id=chat_id, text=archive_url)
        else:
            log('WARNING', 'Invalid URL found', url=url)


@functions_framework.http
def telegram_webhook(request: flask.Request) -> flask.typing.ResponseReturnValue:
    bot = telegram.Bot(token=os.environ["ARCHIVE_BOT_TOKEN"])
    if request.method == "POST":
        try:
            update = telegram.Update.de_json(request.get_json(force=True), bot)
            if not update or not update.message:
                log('WARNING', 'Invalid request format', reason='missing update or message')
                return "Invalid request format", 400
            chat_id = update.message.chat.id
            message_text = update.message.text

            handle_message(bot, chat_id, message_text)
            return "ok"

        except Exception as e:
            log('ERROR', 'Error processing request', error=str(e))
            return "Error processing request", 500
    log('WARNING', 'Invalid request method', method=request.method)
    return "ok"

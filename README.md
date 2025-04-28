# archiveis-tg-bot

A simple Telegram bot to archive URLs in archive.is. The bot is designed to run on Google Cloud Run functions and is particularly useful for bypassing paywalls when using mobile browsers that don't support extensions.

## Features
- Automatically archives any valid URL shared with the bot
- Returns the archived version of the URL
- Runs on Google Cloud Run for serverless operation

## Usage
1. Add the Telegram bot user [@archive_today_bot](https://t.me/archive_today_bot)
2. Share any link that you would like to archive with the bot user
3. The bot will respond with the archived version of your URL

## Deploying Your Own Instance
### Prerequisites
1. Google Cloud account
2. Telegram account
3. Python 3.9 or later
4. Google Cloud SDK installed

### Setup Steps
1. Create a new Telegram bot using [@BotFather](https://t.me/BotFather) and get your bot token
2. Create a new Google Cloud project
3. Enable the Cloud Run API
4. Set up Cloud Run service with the following environment variable:
   - `ARCHIVE_BOT_TOKEN`: Your Telegram bot token

### Deployment
1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Deploy to Cloud Run:
   ```bash
   gcloud run deploy archiveis-bot \
       --set-env-vars "ARCHIVE_BOT_TOKEN=$ARCHIVE_BOT_TOKEN" \
       --runtime python39 \
       --trigger-http \
       --region asia-northeast1 \
       --allow-unauthenticated \
       --source=. \
       --entry-point=telegram_webhook
   ```
4. Set up the webhook URL for your Telegram bot:
   ```bash
   curl -X POST https://api.telegram.org/bot$ARCHIVE_BOT_TOKEN/setWebhook?url=https://your-cloud-run-url
   ```

## Environment Variables
- `ARCHIVE_BOT_TOKEN`: Your Telegram bot token (required)

## Dependencies
- python-telegram-bot==11.1.0
- functions-framework==3.*

## License
This project is licensed under the terms of the included LICENSE file.

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.


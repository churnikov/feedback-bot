# This is a bot that forwards messages to some other places

**Features**:
- Forward messages from bot to some chat or user
- Support replies. When recipient gets message he is able to reply on message. This message will be sent to original sender.
- Self hosted! So only you can access your personal data, unlike [@LivegramBot](https://t.me/@LivegramBot), that [clearly says that they store your data](https://telegra.ph/What-is-Livegram-Bot-03-17. This might me okay for most users. But for others it is unacceptable.

## Setup

**requirements**:
- Docker
- Telegram bot token from [@BotFather](https://t.me/@BotFather)
 

1. Start bot and send to it message or add it to chat that you want messages to be.
2. Then got the following url in browser: `https://api.telegram.org/botBOT_TOKEN:AAG0sqvgocHQXUeK24VjEvuJTm8Qb4gx3HI/getUpdates`
    - Don't forget to set bot api token!
3. Find chat_id field. This will be one of environment variables you'll need to set.

Command to build and run docker container with bot:

```console
docker build -t feedback_bot -f docker/Dockerfile . && docker run --env TG_BOT_TOKEN=FILL_BOT_TOKEN --env TG_CHAT_ID=FILL_CHAT_ID --env COMMAND_REPLIES_PATH=/replies --env BOT_TIMEOUT=10 --env BOT_RETRIES=5 feedback_bot  
``` 

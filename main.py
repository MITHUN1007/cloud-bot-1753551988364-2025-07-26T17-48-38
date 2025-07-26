import os
from telethon import TelegramClient, events
from groq import Groq

# Use environment variables for sensitive information
api_id = int(os.environ.get("TELEGRAM_API_ID"))
api_hash = os.environ.get("TELEGRAM_API_HASH")
bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
groq_api_key = os.environ.get("GROQ_API_KEY")

# Initialize Telegram client
client = TelegramClient('session', api_id, api_hash).start(bot_token=bot_token)

# Initialize Groq client
groq_client = Groq(api_key=groq_api_key)

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond('Hello! I am your auto-reply bot.')

@client.on(events.NewMessage)
async def echo(event):
    # Use Groq to generate a response
    chat_completion = groq_client.chat.completions.create(
        messages=[{"role": "user", "content": event.message.message}],
        model="mixtral-8x7b-32768",
        temperature=0.7,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    await event.respond(chat_completion.choices[0].message.content)

client.run_until_disconnected()
from datetime import datetime
from sys import exit

from decouple import config
from telethon.sessions import StringSession
from telethon.sync import TelegramClient, events

from telegram_bot import TelegramBot

try:
    API_ID = config('API_ID')
    API_HASH = config('API_HASH')
    SESSION = config('SESSION')
    BOT_TOKEN = config('BOT_TOKEN')

    FROM = [int(i) for i in config('CHANNELS_TO_CHECK').split()]
    TO = [int(i) for i in config('CHANNEL_TO_SEND').split()]
except Exception as e:
    print(e)
    exit()

WORDS_TO_CHECK = [i for i in config('TO_CHECK').split('/')]
if WORDS_TO_CHECK[-1] == '':
    WORDS_TO_CHECK = WORDS_TO_CHECK[:-1]


def print_now(content):
    now = datetime.now().strftime("%H:%M:%S")
    print(f'{now} - {content}')


if len(WORDS_TO_CHECK) < 1:
    print_now('no words/phrases found on .env file')
    exit()

if len(FROM) == 0 or len(TO) == 0:
    print_now('FROM or TO on .env file is empty')

try:
    print_now('client starting')
    client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)
    client.start()
    print_now("client has started")
    print_now("bot starting")
    bot = TelegramBot(BOT_TOKEN)
    if bot.verify is False:
        exit()
    print_now("bot has started")
    print_now(f'{len(WORDS_TO_CHECK)} words/phrases found on .env file!')
    _from = [str(i) for i in FROM]
    _to = [str(i) for i in TO]
    print_now(f'check messages from: {", ".join(_from)}')
    print_now(f'and send to: {", ".join(_to)}')
except Exception as error:
    print(error)
    exit()


@client.on(events.NewMessage(incoming=True, chats=FROM))
async def send_vip(event):
    chat = await client.get_entity(event.chat_id)
    for word in WORDS_TO_CHECK:
        msg = event.message.text
        if word in msg.lower():
            text = f'*Message received!*\n\n*Word found*: {word}\n*Group:* {chat.title} ({event.chat_id})\n*Message:*d\n\n' + msg
            bot.send_message(TO, text, print_log='word found')


if __name__ == '__main__':
    client.run_until_disconnected()

import os
from sys import exit


def get_id_hash():
    try:
        API_ID = input('Insert your API ID: ')
        API_HASH = input('Insert your API HASH: ')
        return API_ID, API_HASH
    except:
        exit()


def telethon_session():
    API_ID, API_HASH = get_id_hash()
    try:
        from telethon.sessions import StringSession
        from telethon.sync import TelegramClient
    except ImportError:
        os.system('pip install -U telethon')
        print('Telethon installed')
        from telethon.sessions import StringSession
        from telethon.sync import TelegramClient

    try:
        with TelegramClient(StringSession(), API_ID, API_HASH) as s:
            print('String session generated!')
            print('Insert the string session on .env file')
            print('Your string session:\n')
            print(s.session.save())
    except Exception as error:
        print('An error occured: ', error)


telethon_session()

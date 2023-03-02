import json
import os
import urllib.parse
from datetime import datetime
from time import sleep

import requests


class TelegramBot:
    def __init__(self, token) -> None:
        self.token = token
        self.url = f'https://api.telegram.org/bot{self.token}'
        self.verify = self.auth()

    def print_now(self, content, mode='print'):
        now = datetime.now().strftime("%H:%M:%S")
        print(f'{now} - {content}')
        if mode == 'error':
            if 'log' not in os.listdir():
                f = open('log', 'w')
            else:
                f = open('log', 'a')
            f.write(f'[{now}] - ERROR: {content}\n')
            f.close()

    def auth(self):
        r = requests.get(f'{self.url}/getMe')
        if r.status_code == 200:
            self.print_now('authentication success!')
            return True
        elif r.status_code == 401:
            self.print_now('invalid token', mode='error')
            return False
        elif r.status_code != 200:
            self.print_now(
                f'authentication error! response: {r.json()}', mode='error')
            return False
        else:
            self.print_now(
                f'unknown error, response: {r.json()}', mode='error')
            return False

    def send_message(
            self,
            chat_id: list,
            message: str,
            block_code: bool = False,
            r_status_code=True,
            print_log='message',
            reply=None):
        response_return = []
        message = urllib.parse.quote_plus(message)
        for id in chat_id:
            method = f'/sendMessage?chat_id={id}&text={message}' \
                '&protect_content=True&parse_mode=Markdown&disable_web_page_preview=True'
            if block_code is True:
                method = f'/sendMessage?chat_id={id}&text=`{message}`' \
                    '&protect_content=True&parse_mode=MarkdownV2'
            if reply:
                method += f'&reply_to_message_id={reply}'
            r = requests.post(f'{self.url}{method}')
            if r_status_code is True:
                self.print_now(f'message sent: {print_log} - {r.status_code}')
            else:
                self.print_now(f'message sent: {print_log}')
            if r.status_code != 200:
                self.print_now(content=r.json(), mode='error')
            response_return.append({'chat_id': id, 'response': r.json()})
        return response_return

    def get_updates(self, update_id):
        method = '/getUpdates?timeout=100'
        if update_id:
            method = f'/getUpdates?timeout=100&offset={update_id+1}'
        while True:
            try:
                r = requests.post(f'{self.url}{method}')
                return r.json()
            except Exception as error:
                self.print_now(f'error: {error}')
                sleep(120)

    def set_my_commands(self):
        json_commands = json.dumps(self.commands)
        for chat in self.command_scope:
            json_scope = json.dumps(chat)
            method = f'/setMyCommands?commands={json_commands}&scope={json_scope}'
            requests.post(f'{self.url}{method}')
        self.print_now('done!')

    def delete_my_commands(self):
        command_scope = {
            'type': 'chat',
            'chat_id': 0
        }
        json_scope = json.dumps(command_scope)
        method = f'/deleteMyCommands?scope={json_scope}'
        r = requests.post(f'{self.url}{method}')
        self.print_now(r.json())

    def check_command(self, message):
        try:
            allow_id = [id['chat_id'] for id in self.command_scope]
            chat_id = message['message']['from']['id']
            if chat_id in allow_id:
                if 'entities' in message['message']:
                    if message['message']['entities'][0]['type']  \
                            == 'bot_command':
                        sent_command = message['message']['text'].split(' ')[0]
                        for command in self.commands:
                            if sent_command.replace('/', '') \
                                    == command['command']:
                                return True
            return False
        except KeyError:
            return False

    def listen(self):
        self.print_now('telegram bot online!')
        self.print_now('waiting for message...')
        update_id = None
        while True:
            update = self.get_updates(update_id=update_id)
            messages = update['result']
            if messages:
                for message in messages:
                    if update_id is None:
                        update_id = message['update_id']
                        continue
                    self.print_now(message)
                    update_id = message['update_id']

    def send_image(self, chat_id: list, image_path: str, text=None, print_log='image'):
        results: list = []
        for id in chat_id:
            try:
                files = {'photo': open(image_path, 'rb')}
                if text:
                    data = {'chat_id': id,
                            'caption': text, 'parse_mode': 'Markdown'}
                else:
                    data = {'chat_id': id}
                method = f'{self.url}/sendPhoto'
                r = requests.post(method, files=files, data=data)
                self.print_now(f'image sent: {print_log} - {r.status_code}')
                if r.status_code != 200:
                    self.print_now(content=r.json(), mode='error')
            except Exception as error:
                self.print_now(
                    f'unexpected error {error} - r.json()', mode='error')
            finally:
                results.append(r.json())
        return results

    def send_sticker(self, chat_id: list, sticker_id: str, print_log='sticker'):
        results: list = []
        for id in chat_id:
            try:
                url = f"https://api.telegram.org/bot{self.token}/sendSticker"
                data = {'chat_id': id, 'sticker': sticker_id}
                r = requests.post(url, data=data)
                self.print_now(f'image sent: {print_log} - {r.status_code}')
                if r.status_code != 200:
                    self.print_now(content=r.json(), mode='error')
            except Exception as error:
                self.print_now(
                    f'unexpected error {error} - r.json()', mode='error')
            finally:
                results.append(r.json())
        return results

    def send_button(self, chat_id: list, text: str, keyboard: dict, print_log='button'):
        """
        keyboard example: {"text": "Link", "url": "https://www.google.com"}
        """
        method = f"{self.url}/sendMessage"
        results: list = []
        for chat in chat_id:
            try:
                buttons = json.dumps({'inline_keyboard': [[keyboard]]})
                payload = {"chat_id": chat, "text": text,
                           "reply_markup": buttons, "parse_mode": "Markdown"}
                r = requests.post(method, json=payload)
                self.print_now(f'button sent: {print_log} - {r.status_code}')
                if r.status_code != 200:
                    self.print_now(content=r.json(), mode='error')
            except Exception as error:
                self.print_now(
                    f'unexpected error {error} - r.json()', mode='error')
            finally:
                results.append(r.json())
        return results


# if __name__ == '__main__':
#     bot = TelegramBot('5710072920:AAFA6l4XySdpu4kJytTaq5AYjm5XBZzFw1Y')
#     bot.send_message([-1001725226707], 'Boa noite pessoal!')

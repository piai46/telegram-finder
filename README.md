# Telegram Word Finder

## Setup

### You must have an API ID and API HASH for your account, an Session String and a Bot Token

- To generate an API ID and API HASH, follow the instructions [from official Telegram Website.](https://core.telegram.org/api/obtaining_api_id#obtaining-api-id)
- To create a bot and get your token, follow the instruction [from official Telegram Website.](https://core.telegram.org/bots#how-do-i-create-a-bot)
- To generate an Session String, use the `string_gen.py` file.
- Open `.env` with any text editor and insert `API ID`, `API HASH`, `SESSION` (Session String) and `BOT_TOKEN`.

### Join the groups that interest you and grab their ID
- Open Telegram on your web browser and select the group, look at the web link and grab the ID
![enter image description here](https://i.imgur.com/4wZ90oI.png)
- Add `100` between `-` and `the first ID number`.
E.g. `-1001725226707`
- Add every ID on  `.env` file on `CHANNELS_TO_CHECK` field, separated with space

### Create a channel  to receive notifications and add the bot as admin
- [Create a Telegram channel.](https://telegram.org/faq_channels?setln=en#q-what-39s-a-channel)
- Add the bot that you created as admin.
- Grab the channel ID just like you did before.
- Added the ID to `.env` file on `CHANNEL_TO_SEND` field

### Open `.env` file and insert the key words or phrases
- Open `.env` file and insert the key words or phrases on `CHANNEL_TO_SEND` field, that you want to filter and send to your private channel, always separated by `/`.

### Open cmd and run `pip install -r requirements.txt` to install required libs

## Running

- Run `python main.py` and be happy!
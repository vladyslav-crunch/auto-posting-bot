from telethon.sync import TelegramClient
from telethon.tl import functions, types
from telethon import events, Button
from telethon.types import Message
import ast
from keyGen import keyGenerator
import sys
sys.path.append('./cfg')
import config 
import json
import os
import re
data_path = os.path.join('data', 'data.json')

# Replace 'YOUR_API_KEY' with your actual Telegram Bot API key
client = TelegramClient('bot', config.MANAGER_APP_ID, config.MANAGER_API_HASH).start(bot_token=config.MANAGER_BOT_TOKEN)
# Start the client

client.parse_mode = 'HTML'
client.start()

# Dictionary to store user, message and database states
user_states = {}
message_states={}
user_database = {}

# Define the welcome message
welcome_message = "Добро пожаловать, этот бот создан для управления базой даных для парсинга сообщений. По вопросам работы и пожеланиям обращайтесь к @nero_crunch и @Kubik0n"

#cyrilic checker
def contains_cyrillic(text):

    return bool(re.search(r'[А-Яа-я]', text))

# Start screen

@client.on(events.NewMessage(pattern='/start'))
async def send_welcome(event):
    await event.respond(welcome_message, buttons=keyGenerator("start"))
    user_states[event.chat_id] = None
    user_database[event.chat_id] = None
   

# Main menu screen

@client.on(events.CallbackQuery(pattern=b'menu'))
async def callback(event):
    await client.delete_messages(event.chat_id, event.message_id) 
    await event.respond("Вы находитесь в главном меню управления ботом. Пожалуйста выберите команду, которая вас интересует", buttons = keyGenerator("managing_database"))
    user_states[event.chat_id] = None
    user_database[event.chat_id] = None

# Creating managing screen

@client.on(events.CallbackQuery(pattern=b'managing_database'))
async def callback(event):
    chat_id = event.chat_id
    await client.delete_messages(event.chat_id, event.message_id) 
    await event.respond("Пожалуйста выберите что вы хотите сделать с базой данных", buttons = keyGenerator("managing_database_buttons"))

#user data base handler

@client.on(events.CallbackQuery(pattern=b'add_chanel'))
async def callback(event):
    chat_id = event.chat_id
    await client.delete_messages(event.chat_id, event.message_id) 
    await event.respond("Пожалуйста, напишите канал(ы), которые хотите добавить в формате: \n\nname of account #1\nname of account #2\nname of account #3\n...", buttons = keyGenerator("menu"))
    user_states[chat_id] = "awaiting_adding_chanell_to_database"

# Sending handler

@client.on(events.CallbackQuery(pattern=b'start_sending'))
async def callback(event):
    await client.edit_message(event.sender_id, event.message_id,'Рассылка началась! Подождите, пожалуйста.')
    current_message = message_states[event.chat_id]
    if current_message.grouped_id:
        text_html = repr(current_message.original_update.message.text + "SENDER_ID:" + str(event.chat_id) + 'TO_USERS="' + str(user_database[event.chat_id])+ '"').replace("\\n", "\r\n").replace("'","")
        await client.send_message(entity=config.SPAM_BOT_USERNAME,file=current_message.messages,parse_mode="HTML", message=text_html)
    else:
        text_html = repr(current_message.message.text + "SENDER_ID:" + str(event.chat_id)+ 'TO_USERS="' + str(user_database[event.chat_id])+ '"').replace("\\n", "\r\n").replace("'","")
        await client.send_message(entity = config.SPAM_BOT_USERNAME, message = text_html, parse_mode="html")
    message_states[event.chat_id] = None

# Message (text or image) handler

@client.on(events.NewMessage(func=lambda event: True))
async def handle_message(event):
    if not event.grouped_id:
        if event.chat_id in user_states:
            current_state = user_states[event.chat_id]
            if not event.is_private:
                return
            elif current_state == "awaiting_adding_chanell_to_database":
                chanels_received = repr(event.message.text).replace("\\n", "\r\n").replace("'", "")
                print(chanels_received)
                html_text = "<b>Вы уверены, что хотите добавить именно эты каналы?</b>\r\n\n" + chanels_received 
                await client.send_message(entity=event.chat_id, message=html_text, parse_mode="html", buttons=keyGenerator("confirming_adding_chanel_to_database"))
                # await event.respond('Вы уверены, что хотите добавить именно эты каналы?', buttons=keyGenerator("confirming_adding_chanel_to_database"))
                user_states[event.chat_id] = None
                message_states[event.chat_id] = event.message.message


# Post sending callback handler

@client.on(events.NewMessage(from_users=[config.SPAM_BOT_USERNAME]))
async def handle_message(event):
    try:
        response = ast.literal_eval(event.message.message)
        message = (f'<i>Успешно отправлено</i> <b>{response["sent"]}</b> <i>пользователям,</i> 'f'<i>заблокировано</i> <b>{response["blocked"]}</b>')
        await client.send_message(entity=response["sender_id"], message=message ,parse_mode='html', buttons=keyGenerator("menu"))
    except Exception as e:
        print(e)

# Adding chenell hadnler

@client.on(events.CallbackQuery(pattern=b'adding_chanel_handler'))
async def callback(event):
    await client.edit_message(event.sender_id, event.message_id,'Каналы успешно добалены!', buttons=keyGenerator("menu"))
    current_message = message_states[event.chat_id]
    data_to_add = str(current_message).split()
    print(data_to_add)
    with open(data_path, 'r') as file:
        data = json.load(file)
    for new_channel_name in data_to_add:
        if not(contains_cyrillic(new_channel_name)):
            new_channel = {"channel": new_channel_name}
            data["channels_to_listen"].append(new_channel)
        else:
            pass
    with open(data_path, 'w') as file:
        json.dump(data, file, indent=4)

# Show chanel handler        
@client.on(events.CallbackQuery(pattern=b'show_chanel'))
async def callback(event):
    try:
        with open(data_path, 'r') as file:
            data = json.load(file)

    # Access the "channels_to_listen" array
        channels_to_listen = data["channels_to_listen"]
        channels_show_data = []
    # Iterate through the channels and print each one
        for channel in channels_to_listen:
           channels_show_data.append(channel["channel"])
        print(channels_show_data)
        html_list = '<b>Каналы для парсинга:</b>\n'
        for item in channels_show_data:
            html_list += f'\n&#8226; {item}'
        await client.delete_messages(event.chat_id, event.message_id) 
        await client.send_message(entity=event.chat_id, message=html_list, parse_mode="html")
        await event.respond('Сейчас вы видите все каналы в базе', buttons=keyGenerator("menu"))
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    except FileNotFoundError as e:
        print(f"File not found: {e}")
    except KeyError as e:
        print(f"KeyError: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


# None-stop bot working mode

with client:
    client.run_until_disconnected()



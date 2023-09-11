from telethon.sync import TelegramClient
from telethon.tl import functions, types
from telethon import events, Button
from telethon.types import Message, InputPeerChannel
import ast
import asyncio
from keyGen import keyGenerator
import sys
sys.path.append('./cfg')
import config 
import json
import os
import re


current_directory = os.path.dirname(os.path.abspath(__file__))
root_data_folder = os.path.join(os.path.dirname(current_directory), 'data')
data_path = os.path.join(root_data_folder, 'data.json')
channels_to_listen=[]
channels_to_send=[]


def check_and_update_data():
    if not os.path.exists(root_data_folder):
        os.makedirs(root_data_folder)
    if not os.path.exists(data_path):
        inital_data = {"channels_to_listen":[], "channels_to_send":[]}
        with open(data_path, 'w') as json_file:
            json.dump(inital_data, json_file, indent=4)
    else:
        with open(data_path, 'r') as file:
            data = json.load(file)
            for ctl in data["channels_to_listen"]:
                try:
                    ctle = sender.get_entity(ctl["channel"])
                    channels_to_listen.append(ctle)
                except Exception as e:
                    print(e)
            for cts in data["channels_to_send"]:
                try:
                    ctse = sender.get_entity(cts["channel"])
                    channels_to_send.append(ctse)
                except Exception as e:
                    print(e)

# Replace 'YOUR_API_KEY' with your actual Telegram Bot API key
client = TelegramClient('bot', config.MANAGER_APP_ID, config.MANAGER_API_HASH).start(bot_token=config.MANAGER_BOT_TOKEN)
sender = TelegramClient('sender', config.MANAGER_APP_ID, config.MANAGER_API_HASH)
# Start the client
client.parse_mode = 'HTML'
sender.parse_mode = 'HTML'
client.start()
sender.start()


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

# Creating chanel adding screen

@client.on(events.CallbackQuery(pattern=b'add_chanel'))
async def callback(event):
    chat_id = event.chat_id
    await client.delete_messages(event.chat_id, event.message_id) 
    await event.respond("Пожалуйста, напишите канал(ы), которые хотите добавить в формате: \n\nname of chanel #1\nname of chanel #2\nname of chanel #3\n...", buttons = keyGenerator("menu"))
    user_states[chat_id] = "awaiting_adding_chanel_to_database"

# Creating chanel delete screen

@client.on(events.CallbackQuery(pattern=b'remove_chanel'))
async def callback(event):
    chat_id = event.chat_id
    await client.delete_messages(event.chat_id, event.message_id) 
    await event.respond("Пожалуйста, напишите канал(ы), которые хотите удалить в формате: \n\nname of chanel #1\nname of chanel #2\nname of chanel #3\n...", buttons = keyGenerator("menu"))
    user_states[chat_id] = "awaiting_deleting_chanel_from_database"

# Creating destination screen

@client.on(events.CallbackQuery(pattern=b'change_destination_chanel'))
async def callback(event):
    chat_id = event.chat_id
    await client.delete_messages(event.chat_id, event.message_id) 
    await event.respond("Пожалуйста, напишите канал(ы), в который хотите репостить в формате: \n\nname of chanel #1\nname of chanel #2\nname of chanel #3\n...", buttons = keyGenerator("menu"))
    user_states[chat_id] = "awaiting_changing_destination_channel"

# Message (text or image) handler
@client.on(events.NewMessage(func=lambda event: True))
async def handle_message(event):
    if not event.grouped_id:
        if event.chat_id in user_states:
            current_state = user_states[event.chat_id]
            if not event.is_private:
                return
            elif current_state == "awaiting_adding_chanel_to_database":
                chanels_received = repr(event.message.text).replace("\\n", "\r\n").replace("'", "")
                html_text = "<b>Вы уверены, что хотите добавить именно эты каналы?</b>\r\n\n" + chanels_received  
                await client.send_message(entity=event.chat_id, message=html_text, parse_mode="html", buttons=keyGenerator("confirming_adding_chanel_to_database"))
                user_states[event.chat_id] = None
                message_states[event.chat_id] = event.message.message
            elif current_state == "awaiting_deleting_chanel_from_database":
                chanels_received = repr(event.message.text).replace("\\n", "\r\n").replace("'", "")
                html_text = "<b>Вы уверены, что хотите удалить именно эты каналы?</b>\r\n\n" + chanels_received  
                await client.send_message(entity=event.chat_id, message=html_text, parse_mode="html", buttons=keyGenerator("confirming_removing_chanel_to_database"))
                user_states[event.chat_id] = None
                message_states[event.chat_id] = event.message.message
            elif current_state == "awaiting_changing_destination_channel":
                chanels_received = repr(event.message.text).replace("\\n", "\r\n").replace("'", "")
                html_text = "<b>Вы уверены, что хотите репостить именно в эты каналы?</b>\r\n\n" + chanels_received  
                await client.send_message(entity=event.chat_id, message=html_text, parse_mode="html", buttons=keyGenerator("confirming_changing_destination_channel"))
                user_states[event.chat_id] = None
                message_states[event.chat_id] = event.message.message
        

# Adding chanel handler

@client.on(events.CallbackQuery(pattern=b'adding_chanel_handler'))
async def callback(event):
    await client.edit_message(event.sender_id, event.message_id,'Каналы успешно добалены!', buttons=keyGenerator("menu"))
    current_message = message_states[event.chat_id]
    data_to_add = str(current_message).split()
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
    check_and_update_data()
# Show chanel handler        
@client.on(events.CallbackQuery(pattern=b'show_chanel'))
async def callback(event):
    try:
        with open(data_path, 'r') as file:
            data = json.load(file)

    # Access the "channels_to_listen" array
        channels_to_listen = data["channels_to_listen"]
        channels_to_send = data["channels_to_send"]
        channels_to_listen_data = []
        channels_to_send_data = []
    # Iterate through the channels and print each one

        for channel in channels_to_listen:
           channels_to_listen_data.append(channel["channel"])
        for channel in channels_to_send:
           channels_to_send_data.append(channel["channel"])   
        html_list = '<b>Каналы для парсинга:</b>\n'
        for item in channels_to_listen_data:
            html_list += f'\n&#8226; {item}'


        html_list += '\n\n<b>Каналы назначения:</b>\n'
        for item in channels_to_send_data:
            html_list += f'\n&#8226; {item}'

        await client.delete_messages(event.chat_id, event.message_id) 
        await client.send_message(entity=event.chat_id, message=html_list, parse_mode="html", buttons=keyGenerator("menu"))
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    except FileNotFoundError as e:
        print(f"File not found: {e}")
    except KeyError as e:
        print(f"KeyError: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

#deleting user handler

@client.on(events.CallbackQuery(pattern=b'removing_chanel_handler'))
async def callback(event):
    try:
        with open(data_path, 'r') as file:
            data = json.load(file)

        # Step 2: Identify and remove the channel (e.g., "channel_name_to_delete")
        current_message = message_states[event.chat_id]
        channel_names_to_delete = str(current_message).split()
        if 'channels_to_listen' in data and isinstance(data['channels_to_listen'], list):
            channels_to_listen = data['channels_to_listen']
            updated_channels = [channel for channel in channels_to_listen if channel.get('channel') not in channel_names_to_delete]
            data['channels_to_listen'] = updated_channels
        # Step 4: Write the updated data back to the JSON file
        await client.delete_messages(event.chat_id, event.message_id) 
        await client.send_message(entity=event.chat_id, message="Каналы успешно удалены", parse_mode="html", buttons=keyGenerator("menu"))
        with open(data_path, 'w') as file:
            json.dump(data, file, indent=4)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    except FileNotFoundError as e:
        print(f"File not found: {e}")
    except KeyError as e:
        print(f"KeyError: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    check_and_update_data()
# changing destination channel handler


@client.on(events.CallbackQuery(pattern=b'change_destination_handler'))
async def callback(event):
    try:
        with open(data_path, 'r') as file:
            data = json.load(file)

        # Step 2: Identify and remove the channel (e.g., "channel_name_to_delete")
        current_message = message_states[event.chat_id]
        channel_names_to_set = str(current_message).split()
    # Step 3: Create an array of dictionaries with the specified channel names
        new_channels_to_send = [{"channel": name} for name in channel_names_to_set]

        data["channels_to_send"] = new_channels_to_send

        with open(data_path, 'w') as file:
            json.dump(data, file, indent=4)
        await client.delete_messages(event.chat_id, event.message_id) 
        await client.send_message(entity=event.chat_id, message="Каналы назначения успешно изменены!", parse_mode="html", buttons=keyGenerator("menu"))
            
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    except FileNotFoundError as e:
        print(f"File not found: {e}")
    except KeyError as e:
        print(f"KeyError: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    check_and_update_data()


#Repost everything from channels to listen
@sender.on(events.NewMessage(chats=channels_to_listen))
async def handle_message(event):
    if event.grouped_id:
        return
    for destination_channel in channels_to_send:
        await sender.send_message(entity=destination_channel, message=event.message)

@sender.on(events.Album(chats=channels_to_listen))
async def handle_message(event):
    for destination_channel in channels_to_send:
        await sender.send_message(entity=destination_channel, file=event.messages, message=repr(event.original_update.message.text).replace("'","").replace("\\n","\r\n"), parse_mode="html")

# None-stop bot working mode
check_and_update_data()

with client, sender:
    sender.run_until_disconnected()
    client.run_until_disconnected()




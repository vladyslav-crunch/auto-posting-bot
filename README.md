# auto-posting-bot
Bot which will take messages from another channels and repost it to destination channels

# Telegram Bot Setup Guide

This guide will help you set up a Telegram bot using Python and the Telegram Bot API.

## Prerequisites

Before you begin, make sure you have the following:

- Python installed on your system.

## Step 1: Create a Telegram Bot

1. Open Telegram and search for "@BotFather" or use this [link](https://t.me/BotFather) to open the BotFather chat.

2. Start a chat with BotFather and create a new bot by following the instructions. Once your bot is created, you will receive a token. Copy this token; you'll need it later.

## Step 2: Obtain API Credentials

1. Visit the [Telegram Apps page](https://my.telegram.org/auth?to=apps) and log in with your Telegram account.

2. Enter your phone number and follow the verification process to obtain your App `api_id` and `api_hash`. Also, provide an App title and a Short name.

## Step 3: Set Up Your Environment

1. Edit a `.env` file in the root directory of your project and add the following lines, replacing `<YOUR_BOT_TOKEN>`, `<YOUR_APP_ID>`, and `<YOUR_APP_HASH>` with the values you obtained in the previous steps:

2. Save the `.env` file.

## Step 4: Install Requirements

1. Open your terminal or command prompt.

2. Navigate to the root directory of your project.

3. Run the following command to install all the required dependencies from `requirements.txt`:

```bash

pip install -r requirements.txt
```
## Step 5: Run Your Bot

1. Open your terminal or command prompt.

2. Navigate to the root directory of your project.

3. Run the following command to start your bot:

```bash
python ./bot/main.py
```
4. Enter your phone number and follow the verification process

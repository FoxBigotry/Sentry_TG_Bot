# Telegram Sentry Integration
This project provides an integration between Sentry and Telegram for notifying about errors via a Telegram bot.

## Table of Contents
- [Technologies](#Technologies)
- [Installation and Setup](#Installation and Setup)
- [Running the Project](#Installation Steps)
- [Setting Up Telegram Bot Webhook](#Setting Up Telegram Bot Webhook)
- [Project Structure](#Project Structure)
- [To do](#to-do)


## Technologies
The project uses the following technologies and libraries:

- Python
- FastAPI
- aiogram
- Motor (asynchronous MongoDB client)
- Pydantic

## Installation and Setup
Prerequisites
- Python 3.8 or higher
- MongoDB

## Installation Steps
1. Clone the repository
```sh
git clone https://github.com/FoxBigotry/Sentry_TG_Bot.git
```

2. Configure environment variables
```sh
TG_KEY=your_telegram_bot_token
CHAT_ID=your_telegram_chat_id
MONGO_URI=your_mongodb_uri
MONGO_DB_NAME=your_mongodb_database_name
```

## Running the Project
Start the application
```sh
uvicorn main:app --reload
```

## Setting Up Telegram Bot Webhook
To set up the Telegram bot webhook, run the following PowerShell commands:
```sh
$url = "https://api.telegram.org/bot<your-telegram-bot-token>/setWebhook"
$body = @{
    url = "https://<your-ngrok-url>/webhook/<your-telegram-bot-token>"
}

Invoke-RestMethod -Uri $url -Method Post -ContentType "application/x-www-form-urlencoded" -Body $body
```

## Project Structure

- `main.py` - Main FastAPI application file.
- `bot/`
  - `bot.py` - Contains the logic for the Telegram bot, including:
    - Creating new topics in the group.
    - Sending messages to a specific chat or topic.
- `database/` - MongoDB models and operations.
  - `connect.py` - Database connection and functions for working with collections.
  - `models.py` - Error model definition.
- `webhooks/`
  - `utils` - Contains utility functions for processing Sentry payloads and interacting with MongoDB.
  - `webhook` - Webhook handling logic for Sentry and Telegram.
- `settings.py` - Application settings loaded from the .env file.

## To do
- Logger
- Migrate the database from MongoDB to Tortoise ORM.

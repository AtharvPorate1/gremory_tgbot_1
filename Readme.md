# Telegram Liquidity Management Bot

A Telegram bot for managing liquidity pools and agents, built with Python Flask and pyTelegramBotAPI.

## Features

- User authentication via email
- View agent balances
- List user agents
- (Coming soon) Liquidity pool management
- (Coming soon) Search functionality
- (Coming soon) Advanced prompts

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- A Telegram bot token (get from [BotFather](https://t.me/BotFather))
- HTTPS endpoint for webhook (can use Ngrok for development)

### Installation

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and fill in your values:
   ```
   cp .env.example .env
   ```
4. Edit `.env` with your Bot Token and webhook URL

### Running the Bot

For development with Ngrok:
1. Start Ngrok on your chosen port:
   ```
   ngrok http 5000
   ```
2. Update the `WEBHOOK_URL` in `.env` with your Ngrok HTTPS URL
3. Run the Flask app:
   ```
   python app.py
   ```
4. Visit `https://your-ngrok-url/set_webhook` to set up the webhook

For production:
1. Deploy to your server
2. Set up HTTPS
3. Configure your production `WEBHOOK_URL`
4. Run with gunicorn:
   ```
   gunicorn app:app
   ```

## Project Structure

- `app.py` - Main application with Flask and Telegram bot handlers
- `database.py` - Mock database for development (replace with real DB in production)
- `.env` - Environment variables
- `requirements.txt` - Python dependencies

## Usage

1. Start the bot by sending `/start`
2. Connect with your email address
3. Use the menu buttons to navigate the features# gremory_tgbot_1

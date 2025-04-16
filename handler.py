import os
import telebot
import logging
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    raise ValueError("No BOT_TOKEN found in environment variables")

bot = telebot.TeleBot(BOT_TOKEN)

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def superhandler(text):
    print("received text:", text)
    if text == "/start":
        try:
            bot.send_message(
                "5284739416",
                "Welcome to the Liquidity Management Bot! To get started, please connect your account.",
            )
            logger.info("Welcome message sent to 5284739416")
        except Exception as e:
            logger.error(f"Error sending welcome message: {str(e)}")

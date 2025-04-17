# app.py
import os
from flask import Flask, request, jsonify
import telebot
from telebot import types
import logging
from dotenv import load_dotenv
import json
from utils.handler import superhandler


# Database simulation (in a real app, you would use a proper database)
from database import users, agents, balances

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Initialize Telegram bot with your token
BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    raise ValueError("No BOT_TOKEN found in environment variables")

bot = telebot.TeleBot(BOT_TOKEN)
WEBHOOK_URL = os.getenv('WEBHOOK_URL', 'https://your-domain.com/webhook')
print(WEBHOOK_URL)

# Set webhook
@app.route('/set_webhook', methods=['GET'])
def set_webhook():
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)
    return "Webhook set"

# Process webhook

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        try:
            json_string = request.get_data().decode('utf-8')
            print(f"Received webhook data: {json_string}")  # Print raw data for inspection
            update = telebot.types.Update.de_json(json_string)
            bot.process_new_updates([update])
            print("Update processed successfully")
            data = json.loads(json_string)
            text = data["message"]["text"]
            print("recieved : ", text)
            superhandler(text)
            print("superhandler called succesfully ")
            return jsonify({'status': 'ok'})
        except Exception as e:
            print(f"Error processing update: {str(e)}")
            # Return 200 even if there's an error to prevent Telegram from retrying
            return jsonify({'status': 'error', 'error': str(e)})
    else:
        print(f"Invalid content-type: {request.headers.get('content-type')}")
        return jsonify({'status': 'error', 'message': 'Invalid content-type'})







### The code below should be converted to functions and used appropriately



# Start command handler
@bot.message_handler(commands=['start'])
def start(message):
    logger.info(f"Received /start command from user {message.from_user.id}")
    user_id = message.from_user.id
    
    # Check if user already exists
    if user_id in users:
        logger.info(f"User {user_id} exists, showing main menu")
        main_menu(message)
    else:
        logger.info(f"New user {user_id}, showing welcome message")
        # Welcome message with connect button
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        connect_button = types.KeyboardButton('Connect')
        markup.add(connect_button)
        
        try:
            bot.send_message(
                message.chat.id,
                "Welcome to the Liquidity Management Bot! To get started, please connect your account.",
                reply_markup=markup
            )
            logger.info(f"Welcome message sent to {message.chat.id}")
        except Exception as e:
            logger.error(f"Error sending welcome message: {str(e)}")
# Handle 'Connect' button
@bot.message_handler(func=lambda message: message.text == 'Connect')
def request_email(message):
    bot.send_message(
        message.chat.id,
        "Please enter your email address to connect:"
    )
    bot.register_next_step_handler(message, process_email)

# Process email
def process_email(message):
    email = message.text
    user_id = message.from_user.id
    
    # Validate email (basic validation)
    if '@' not in email or '.' not in email:
        bot.send_message(
            message.chat.id,
            "Invalid email format. Please try again with a valid email address."
        )
        bot.register_next_step_handler(message, process_email)
        return
    
    # Store user data (in a real app, you would save this to a database)
    users[user_id] = {
        'email': email,
        'chat_id': message.chat.id
    }
    
    bot.send_message(
        message.chat.id,
        f"Thank you! Your account with email {email} has been connected successfully."
    )
    
    # Show main menu
    main_menu(message)

# Main menu
def main_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    
    # Add buttons for each option
    balance_button = types.KeyboardButton('Show Balance')
    agents_button = types.KeyboardButton('Your Agents')
    liquidity_pools_button = types.KeyboardButton('Show Liquidity Pools')
    search_button = types.KeyboardButton('Search Liquidity Pools')
    prompt_button = types.KeyboardButton('Prompt')
    
    markup.row(balance_button)
    markup.row(agents_button)
    markup.row(liquidity_pools_button)
    markup.row(search_button)
    markup.row(prompt_button)
    
    bot.send_message(
        message.chat.id,
        "Welcome to the main menu. Please select an option:",
        reply_markup=markup
    )

# Handle 'Show Balance' button
@bot.message_handler(func=lambda message: message.text == 'Show Balance')
def show_balance(message):
    user_id = message.from_user.id
    
    # Check if user exists
    if user_id not in users:
        bot.send_message(
            message.chat.id,
            "You are not connected. Please use /start to connect your account."
        )
        return
    
    # Get user's agents and their balances
    user_agents = agents.get(user_id, [])
    
    if not user_agents:
        bot.send_message(
            message.chat.id,
            "You don't have any agents yet."
        )
        return
    
    # Prepare balance information
    balance_text = "📊 *Your Balance Report*\n\n"
    total_balance = 0
    
    for agent_id in user_agents:
        agent_balance = balances.get(agent_id, 0)
        total_balance += agent_balance
        balance_text += f"Agent {agent_id}: *{agent_balance:.2f} USDT*\n"
    
    balance_text += f"\n*Total Balance: {total_balance:.2f} USDT*"
    
    bot.send_message(
        message.chat.id,
        balance_text,
        parse_mode='Markdown'
    )

# Handle 'Your Agents' button
@bot.message_handler(func=lambda message: message.text == 'Your Agents')
def your_agents(message):
    user_id = message.from_user.id
    
    # Check if user exists
    if user_id not in users:
        bot.send_message(
            message.chat.id,
            "You are not connected. Please use /start to connect your account."
        )
        return
    
    # Get user's agents
    user_agents = agents.get(user_id, [])
    
    if not user_agents:
        bot.send_message(
            message.chat.id,
            "You don't have any agents yet."
        )
        return
    
    # Prepare agents information
    agents_text = "🤖 *Your Agents*\n\n"
    
    for agent_id in user_agents:
        agents_text += f"Agent {agent_id}\n"
    
    bot.send_message(
        message.chat.id,
        agents_text,
        parse_mode='Markdown'
    )

# Handle 'Show Liquidity Pools' button
@bot.message_handler(func=lambda message: message.text == 'Show Liquidity Pools')
def show_liquidity_pools(message):
    bot.send_message(
        message.chat.id,
        "Liquidity pools feature will be implemented soon."
    )

# Handle 'Search Liquidity Pools' button
@bot.message_handler(func=lambda message: message.text == 'Search Liquidity Pools')
def search_liquidity_pools(message):
    bot.send_message(
        message.chat.id,
        "Search liquidity pools feature will be implemented soon."
    )

# Handle 'Prompt' button
@bot.message_handler(func=lambda message: message.text == 'Prompt')
def prompt(message):
    bot.send_message(
        message.chat.id,
        "Prompt feature will be implemented soon."
    )

# Handle help command
@bot.message_handler(commands=['help'])
def help_command(message):
    help_text = """
*Available Commands:*
/start - Start the bot and connect your account
/help - Show this help message
    
*Available Buttons:*
- Show Balance - Display your agents' balances
- Your Agents - List your active agents
- Show Liquidity Pools - View available liquidity pools
- Search Liquidity Pools - Search for specific pools
- Prompt - Additional options
    """
    bot.send_message(
        message.chat.id,
        help_text,
        parse_mode='Markdown'
    )

# Handle unknown commands/messages
@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_all(message):
    print(f"Received message: {message.text} from {message.chat.id}")
    try:
        bot.reply_to(message, "I received your message")
        print("Reply sent successfully")
    except Exception as e:
        print(f"Error sending reply: {str(e)}")

# Run the app
if __name__ == '__main__':
    # Run Flask app
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
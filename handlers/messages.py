from config import BOT_TOKEN, BOT_USERNAME
from telegram import Update
from telegram.ext import ContextTypes
from handlers.token import handle_amount_input, handle_token_message

def handle_response(text: str) -> str:
    processed = text.lower()
    
    if "hello" in processed:
        return "Hey there!"
    
    if "how are you" in processed:
        return "I'm a bot, so I'm always good!"
    
    return "I don't understand what you wrote..."

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_text = update.message.text.strip()
    
    # Check if we're expecting an amount input
    if context.user_data.get('awaiting_amount'):
        return await handle_amount_input(update, context)
    
    # Otherwise, check for token address
    if len(message_text) == 44 and message_text.isalnum():
        await handle_token_message(update, context)
    else:
        await update.message.reply_text("❗️ Please enter a valid Solana token address (44 alphanumeric characters).")
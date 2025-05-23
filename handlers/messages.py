from config import BOT_TOKEN, BOT_USERNAME
from telegram import Update
from telegram.ext import ContextTypes


def handle_response(text: str) -> str:
    processed = text.lower()
    
    if "hello" in processed:
        return "Hey there!"
    
    if "how are you" in processed:
        return "I'm a bot, so I'm always good!"
    
    return "I don't understand what you wrote..."

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type = update.message.chat.type
    text = update.message.text
    
    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')
    
    if message_type == "group":
        if BOT_USERNAME in text:
            new_text = text.replace(BOT_USERNAME, "").strip()
            response = handle_response(new_text)
        else:
            return
    else:
        response = handle_response(text)
        
    print("Bot:", response)
    await update.message.reply_text(response)
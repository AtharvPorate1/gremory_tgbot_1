from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from config import BOT_TOKEN
from handlers.commands import start_command, open_command
from handlers.messages import handle_message
from handlers.errors import error
from handlers.token import handle_token_message, token_button_callback

if __name__ == "__main__":
    print("Starting bot...")
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Commands
    app.add_handler(CommandHandler("start", start_command))
    # app.add_handler(CommandHandler("help", help_command))
    # app.add_handler(CommandHandler("custom", custom_command))
    # Add this to where you register command handlers
    app.add_handler(CommandHandler("open", open_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(token_button_callback))


    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    
    # Errors
    app.add_error_handler(error)
    
    print("Polling...")
    app.run_polling(poll_interval=3)
# handlers/commands.py
from telegram import Update
from telegram.ext import ContextTypes
from handlers.templates import WELCOME_EXISTING_USER, WELCOME_NEW_USER, WALLET_CREATED
from utils.user import check_user_in_db, get_wallet_address, create_new_user

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tgId = update.effective_user.id
    username = update.effective_user.username or "no username"
    print(f"User {tgId} started the bot.")
    
    # Check if user exists in DB (pseudo-code)
    user_exists = await check_user_in_db(tgId)  # You'll need to implement this


    if user_exists["exists"]:
        print("User exists in DB:", username)
        wallet_address = await get_wallet_address(tgId)  # Implement this
        print("User's wallet address:", wallet_address)
        await update.message.reply_text(
            WELCOME_EXISTING_USER.format(wallet_address=wallet_address),
            parse_mode='Markdown'
        )
    else:
        # Show creating wallet message
        await update.message.reply_text(WELCOME_NEW_USER)
        print("Creating new wallet for user:", username)
        # Simulate wallet creation (replace with actual logic)
        response = await create_new_user(tgId, username)  # Implement this
        print("New user response:", response)
        print(" new wallet address : ", response["wallet"]["address"])
        wallet_address = response["wallet"]["address"]
        # Send wallet created message
        await update.message.reply_text(
            WALLET_CREATED.format(wallet_address=wallet_address),
            parse_mode='Markdown'
        )
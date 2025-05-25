# handlers/commands.py
from telegram import Update
from telegram.ext import ContextTypes
from handlers.templates import WELCOME_EXISTING_USER, WELCOME_NEW_USER, WALLET_CREATED, TRENDING_POOLS_MESSAGE, POOL_INFO_TEMPLATE
from utils.user import check_user_in_db, get_wallet_address, create_new_user
from lib.wallet import get_sol_balance  # Assuming you have a function to get SOL balance
from lib.meteora import get_trending_pools

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tgId = update.effective_user.id
    username = update.effective_user.username or "no username"
    print(f"User {tgId} started the bot.")
    
    # Check if user exists in DB (pseudo-code)
    user_exists = await check_user_in_db(tgId)  # You'll need to implement this


    if user_exists["exists"]:
        print("User exists in DB:", username)
        wallet_address = await get_wallet_address(tgId)  # Implement this
        print("User's wallet address:", wallet_address["walletAddress"])
        sol_balance = get_sol_balance(wallet_address["walletAddress"])  # Implement this
        await update.message.reply_text(
            WELCOME_EXISTING_USER.format(wallet_address=wallet_address["walletAddress"], balance=sol_balance),
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
        sol_balance = get_sol_balance(wallet_address)
        # Send wallet created message
        await update.message.reply_text(
            WALLET_CREATED.format(wallet_address=wallet_address, balance=sol_balance ),
            parse_mode='Markdown'
        )


async def open_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Get trending pools
        pools = get_trending_pools()
        
        # Format each pool's information
        pool_list = []
        for pool in pools['pairs']:
            # Calculate market cap (simplified as reserve_y_amount * current_price)
            market_cap = pool['reserve_y_amount'] * pool['current_price']
            
            pool_info = POOL_INFO_TEMPLATE.format(
                name=pool['name'],
                dex_link="https://meteora.ag",  # Placeholder link
                market_cap=market_cap,
                volume_24h=pool['trade_volume_24h']
            )
            pool_list.append(pool_info)
        
        # Send the formatted message
        await update.message.reply_text(
            TRENDING_POOLS_MESSAGE.format(pool_list="\n".join(pool_list)),
            parse_mode='Markdown',
            disable_web_page_preview=True
        )
        
    except Exception as e:
        print(f"Error in open_command: {e}")
        await update.message.reply_text(
            "⚠️ Could not fetch trending pools. Please try again later."
        )

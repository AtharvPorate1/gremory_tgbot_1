from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import requests
from handlers.templates import TOKEN_INFO_TEMPLATE, OPEN_POSITION, BUY_1_SOL, BUY_X_SOL, SELL_50, SELL_100, CLOSE, REFRESH
from utils.ca_finder import fetch_token_info

async def handle_token_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_text = update.message.text.strip()
    print(f"Received message: {message_text}")
    # Check if the message looks like a token address
    if len(message_text) == 44 and message_text.isalnum():
        try:
            # Fetch token info from API
            print(f"Fetching token info for: {message_text}")
            token_info = fetch_token_info(message_text)
            
            if token_info:
                # Create reply with buttons
                keyboard = [
                    [
                        InlineKeyboardButton(OPEN_POSITION, callback_data=f"open_{message_text}"),
                        InlineKeyboardButton(BUY_1_SOL, callback_data=f"buy1_{message_text}"),
                    ],
                    [
                        InlineKeyboardButton(BUY_X_SOL, callback_data=f"buyx_{message_text}"),
                        InlineKeyboardButton(SELL_50, callback_data=f"sell50_{message_text}"),
                    ],
                    [
                        InlineKeyboardButton(SELL_100, callback_data=f"sell100_{message_text}"),
                        InlineKeyboardButton(CLOSE, callback_data=f"close_{message_text}"),
                    ],
                    [
                        InlineKeyboardButton(REFRESH, callback_data=f"refresh_{message_text}"),
                    ]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                # Format the token info message with available data
                formatted_message = TOKEN_INFO_TEMPLATE.format(
                    name=token_info.get('name', 'Unknown'),
                    symbol=token_info.get('symbol', 'Unknown'),
                    address=message_text,
                    explorer_url=f"https://solscan.io/token/{message_text}",
                    dexscreener_url=f"https://dexscreener.com/solana/{message_text}",
                    price=token_info.get('price', 0),
                    mcap=token_info.get('mcap', 0),  # Will be 0 since not available
                    price_30m=token_info.get('fee_tvl_ratio_30m', 0),  # Using fee_tvl_ratio as proxy
                    price_1h=token_info.get('fee_tvl_ratio_1h', 0),
                    price_4h=token_info.get('fee_tvl_ratio_4h', 0),
                    price_24h=token_info.get('fee_tvl_ratio_24h', 0),
                    volume_30m=token_info.get('volume_30m', 0) / 1000 if token_info.get('volume_30m') else 0,  # Convert to K
                    volume_1h=token_info.get('volume_1h', 0) / 1000 if token_info.get('volume_1h') else 0,
                    volume_4h=token_info.get('volume_4h', 0) / 1000 if token_info.get('volume_4h') else 0,
                    volume_24h=token_info.get('volume_24h', 0) / 1000000 if token_info.get('volume_24h') else 0,  # Convert to M
                    balance=0,  # Not available in current data
                    balance_value=0   # Not available in current data
                )
                
                await update.message.reply_text(
                    formatted_message,
                    parse_mode='Markdown',
                    disable_web_page_preview=True,
                    reply_markup=reply_markup
                )
            else:
                await update.message.reply_text("❌ Token not found or invalid contract address.")
                
        except Exception as e:
            print(f"Error processing token: {e}")
            await update.message.reply_text("⚠️ Error fetching token information. Please try again later.")
    else:
        await update.message.reply_text("❗️ Please enter a valid Solana token address (44 alphanumeric characters).")



async def token_button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    action, token_address = query.data.split('_', 1)
    
    if action == 'refresh':
        # Re-fetch token info
        token_info = fetch_token_info(token_address)
        # Update the message with fresh data
        # (similar to handle_token_message but editing existing message)
        
    elif action == 'open':
        # Handle open position
        await query.edit_message_text(text=f"Opening position for {token_address}...")
        
    elif action == 'buy1':
        # Handle buy 1 SOL worth
        await query.edit_message_text(text=f"Buying 1 SOL worth of {token_address}...")
        
    # Implement other actions similarly...
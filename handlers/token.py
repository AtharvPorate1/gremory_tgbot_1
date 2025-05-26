from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import requests
from handlers.templates import TOKEN_INFO_TEMPLATE, OPEN_POSITION, BUY_1_SOL, BUY_X_SOL, SELL_50, SELL_100, CLOSE, REFRESH
from utils.ca_finder import fetch_token_info
from utils.user import get_agent_link
import aiohttp
from aiohttp import TCPConnector
import ssl



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


async def handle_amount_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    amount_text = update.message.text.strip()
    
    if amount_text.replace('.', '').isdigit():  # Basic number validation
        try:
            amount = float(amount_text)
            context.user_data['position_amount'] = amount
            context.user_data['awaiting_amount'] = False  # Clear the flag
            context.user_data['awaiting_strategy'] = True
            
            # Show strategy selection buttons
            keyboard = [
                [InlineKeyboardButton("⚖️ Balanced", callback_data="strategy_balanced")],
                [InlineKeyboardButton("⚡ Imbalanced (Coming Soon)", callback_data="strategy_imbalanced")],
                [InlineKeyboardButton("📈 Curve (Coming Soon)", callback_data="strategy_curve")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(
                text=f"🔮 Select strategy for {amount} SOL investment:",
                reply_markup=reply_markup
            )
            
        except ValueError:
            await update.message.reply_text("❌ Please enter a valid number for the amount in SOL")
    else:
        await update.message.reply_text("❌ Please enter a valid amount in SOL")
 
async def token_button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    # Check if we're in the amount input stage
    if context.user_data.get('awaiting_amount'):
        return await handle_amount_input(update, context)
    
    # Check if we're in the strategy selection stage
    if context.user_data.get('awaiting_strategy'):
        return await handle_strategy_selection(update, context)
    
    # Original button handling
    action, token_address = query.data.split('_', 1)
    
    if action == 'refresh':
        token_info = fetch_token_info(token_address)
        # Update message with fresh data
        await refresh_token_message(query, token_info, token_address)
        
    elif action == 'open':
        # Store token address in context for the multi-step process
        context.user_data['current_token'] = token_address
        context.user_data['awaiting_amount'] = True
        
        await query.edit_message_text(
            text=f"💵 Enter amount in SOL to invest in {token_address.split('-')[0] if '-' in token_address else token_address[:4]}...",
            reply_markup=None
        )
        
    elif action == 'buy1':
        # Handle buy 1 SOL worth immediately
        await execute_trade(query, token_address, amount=1, strategy='balanced')
        
    # Other actions remain the same...



async def handle_strategy_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data.startswith('strategy_'):
        strategy = query.data.split('_')[1]
        
        if strategy in ['imbalanced', 'curve']:
            await query.edit_message_text("⏳ This strategy is coming soon!")
            return
            
        token_address = context.user_data['current_token']
        amount = context.user_data['position_amount']
        
        # Clear the state
        context.user_data.clear()
        
        # Execute the trade with collected parameters
        await execute_trade(query, token_address, amount, strategy)

async def execute_trade(query, token_address, amount, strategy):
    agent_link = await get_agent_link(query.from_user.id)
    pool_address = token_address
    
    # Create SSL context that doesn't verify certificates
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    # Build detailed prompt
    prompt = (
        f"Open {strategy} position in pool {pool_address} with {amount} SOL. "
        f"Token: {token_address.split('-')[0] if '-' in token_address else token_address[:4]}. "
        f"Strategy parameters: {get_strategy_params(strategy)}"
    )
    
    payload = {
        "prompt": prompt,
        "metadata": {
            "action": "open_position",
            "amount_sol": amount,
            "strategy": strategy,
            "pool_address": pool_address
        }
    }
    
    try:
        # Create custom connector with our SSL context
        connector = TCPConnector(ssl=ssl_context)
        
        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.post(
                f'{agent_link["agentLink"]}/api/agent/prompt',
                json=payload,
                timeout=aiohttp.ClientTimeout(total=30)
            ) as resp:
                if resp.status == 200:
                    result = await resp.json()
                    success_message = (
                        f"✅ Successfully opened {strategy} position with {amount} SOL!\n"
                        f"Tx: {result.get('tx_hash', 'Not available')}\n"
                        f"Position: {result.get('position_address', 'Not available')}"
                    )
                    # await query.edit_message_text(text=success_message)
                else:
                    error_text = await resp.text()
                    error_message = (
                        f"❌ Failed to open position (Status: {resp.status}).\n"
                        f"Error: {error_text[:200]}"  # Truncate long error messages
                    )
                    await query.edit_message_text(text=error_message)
                    
    except aiohttp.ClientError as e:
        error_message = (
            f"⚠️ Network error executing trade:\n"
            f"{str(e)}\n\n"
            f"Please try again later."
        )
        await query.edit_message_text(text=error_message)
        
    except Exception as e:
        error_message = (
            f"⚠️ Unexpected error executing trade:\n"
            f"{str(e)}\n\n"
            f"Please contact support if this persists."
        )
        await query.edit_message_text(text=error_message)



def get_strategy_params(strategy):
    """Return strategy-specific parameters"""
    strategies = {
        'balanced': {
            'price_range': 'full_range',
            'rebalance_threshold': '5%',
            'fee_tier': 'auto_select'
        },
        'imbalanced': {
            'price_range': 'concentrated',
            'direction': 'upward_bias',
            'rebalance_threshold': '10%'
        },
        'curve': {
            'curve_type': 'dynamic',
            'adjustment_sensitivity': 'medium'
        }
    }
    return strategies.get(strategy, {})

async def refresh_token_message(query, token_info, token_address):
    """Refresh the token info message while keeping the buttons"""
    # Recreate the original message with updated data
    formatted_message = TOKEN_INFO_TEMPLATE.format(
        name=token_info.get('name', 'Unknown'),
        symbol=token_info.get('symbol', 'Unknown'),
        address=token_address,
        explorer_url=f"https://solscan.io/token/{token_address}",
        dexscreener_url=f"https://dexscreener.com/solana/{token_address}",
        price=token_info.get('price', 0),
        mcap=token_info.get('mcap', 0),
        price_30m=token_info.get('fee_tvl_ratio_30m', 0),
        price_1h=token_info.get('fee_tvl_ratio_1h', 0),
        price_4h=token_info.get('fee_tvl_ratio_4h', 0),
        price_24h=token_info.get('fee_tvl_ratio_24h', 0),
        volume_30m=token_info.get('volume_30m', 0) / 1000 if token_info.get('volume_30m') else 0,
        volume_1h=token_info.get('volume_1h', 0) / 1000 if token_info.get('volume_1h') else 0,
        volume_4h=token_info.get('volume_4h', 0) / 1000 if token_info.get('volume_4h') else 0,
        volume_24h=token_info.get('volume_24h', 0) / 1000000 if token_info.get('volume_24h') else 0,
        balance=0,
        balance_value=0
    )
    
    # Recreate the original buttons
    keyboard = [
        [InlineKeyboardButton(OPEN_POSITION, callback_data=f"open_{token_address}"),
         InlineKeyboardButton(BUY_1_SOL, callback_data=f"buy1_{token_address}")],
        [InlineKeyboardButton(BUY_X_SOL, callback_data=f"buyx_{token_address}"),
         InlineKeyboardButton(SELL_50, callback_data=f"sell50_{token_address}")],
        [InlineKeyboardButton(SELL_100, callback_data=f"sell100_{token_address}"),
         InlineKeyboardButton(CLOSE, callback_data=f"close_{token_address}")],
        [InlineKeyboardButton(REFRESH, callback_data=f"refresh_{token_address}")]
    ]
    
    await query.edit_message_text(
        text=formatted_message,
        parse_mode='Markdown',
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
# handlers/templates.py

WELCOME_EXISTING_USER = """🏝️ Welcome to Gremory.ai: the easiest way to LP on Solana DEXes!

Wallet Address: `{wallet_address}` (tap to copy)
Wallet Balance: {balance} SOL

Get started by depositing SOL in your wallet address.

Use /open or enter token address in bot chat to create new positions!"""

WELCOME_NEW_USER = """🏝️ Welcome to Gremory.ai!

Creating a new wallet for you...
⏳ Please wait while we set things up.

You'll be able to:
• Provide liquidity on Solana DEXes
• Earn trading fees
• Manage positions easily"""

WALLET_CREATED = """✅ Wallet created successfully!

Your new wallet address:
`{wallet_address}` (tap to copy)
Wakket Balance: {balance} SOL

Deposit SOL to this address to get started!
Use /open to create your first position."""


# Add this to handlers/templates.py
TRENDING_POOLS_MESSAGE = """Enter CA or meteora link in bot chat or choose a token from the below trending list:

{pool_list}
"""

POOL_INFO_TEMPLATE = """/[{index} {name}](https://t.me/cleopetra_bot?start=token_{token_address}) | Mcap: ${market_cap} | Volume 24h: ${volume_24h} | [Dex]({dex_link})"""




TOKEN_INFO_TEMPLATE = """*{name} | {symbol} | {address}*

[Explorer]({explorer_url}) | [Dexscreener]({dexscreener_url})

*Price:* ${price:,.5f}
*Mcap:* ${mcap:,.3f}M

*Fee_TVL ratio:*
30m: {price_30m}%, 1h: {price_1h}%, 4h: {price_4h}%, 24h: {price_24h}%

*Volume Stats:*
30m: ${volume_30m}K, 1h: ${volume_1h}K, 4h: ${volume_4h}K, 24h: ${volume_24h}M

*Wallet balance:* {balance} {symbol} (${balance_value})
"""

# Button texts
OPEN_POSITION = "📈 Open Position"
BUY_1_SOL = "🛒 Buy 1 SOL"
BUY_X_SOL = "💵 Buy X SOL"
SELL_50 = "💰 Sell 50%"
SELL_100 = "💸 Sell 100%"
CLOSE = "❌ Close"
REFRESH = "🔄 Refresh"
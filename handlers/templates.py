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
TRENDING_POOLS_MESSAGE = """📊 *Top Trending Pools*

{pool_list}

Click on a pool name to select it.
"""

POOL_INFO_TEMPLATE = """🔹 *[{name}]({dex_link})*
- Market Cap: ${market_cap:,.2f}
- 24h Volume: ${volume_24h:,.2f}
"""
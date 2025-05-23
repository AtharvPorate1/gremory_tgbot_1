# handlers/templates.py

WELCOME_EXISTING_USER = """🏝️ Welcome to Gremory.ai: the easiest way to LP on Solana DEXes!

Wallet Address: `{wallet_address}` (tap to copy)

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

Deposit SOL to this address to get started!
Use /open to create your first position."""
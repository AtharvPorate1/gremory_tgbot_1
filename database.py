# database.py
"""
This module simulates a database for the Telegram bot.
In a production environment, you would replace this with a real database.
"""

# Store user information
users = {}

# Map user_id to a list of agent_ids
agents = {
    123456789: ['agent1', 'agent2'],  # Sample data
}

# Map agent_id to balance in USDT
balances = {
    'agent1': 1500.75,
    'agent2': 2350.25,
}
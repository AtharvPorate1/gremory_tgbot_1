from solana.rpc.api import Client
from solders.pubkey import Pubkey  # Correct import for Pubkey


def get_sol_balance(wallet_address):
    # Connect to Solana mainnet
    solana_client = Client("https://api.mainnet-beta.solana.com")

    try:
        # Convert base58 address to Pubkey
        pubkey = Pubkey.from_string(wallet_address)
        
        # Get SOL balance (in lamports)
        balance_response = solana_client.get_balance(pubkey)
        lamports = balance_response.value
        sol_balance = lamports / 10**9  # Convert lamports to SOL

        print(f"Wallet: {wallet_address}")
        print(f"SOL Balance: {sol_balance:.6f} SOL")

        return sol_balance  # ✅ Missing return

    except Exception as e:
        print(f"Error fetching balance: {e}")
        return 0  # Optionally return 0 or None on error

   
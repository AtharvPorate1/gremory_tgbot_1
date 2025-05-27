import requests
import requests
from bs4 import BeautifulSoup
import json



def get_trending_pools():
    url = "https://dlmm-api.meteora.ag/pair/all_with_pagination"
    params = {
        "limit": 3,
        "sort_key": "feetvlratio2h"
    }
    response = requests.get(url, params=params)
    print(response.json())
    response.raise_for_status()
    return response.json()

# get_trending_pools()



def get_solana_meteora_pairs():
    url = 'https://dexscreen-scraper.vercel.app/dex'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract JSON data
    json_data = soup.find('pre', {'id': 'jsonData'}).text
    data = json.loads(json_data)

    # Filter for Solana/Meteora pairs
    filtered_pairs = [
        pair for pair in data['data']
        if pair.get('chainId') == 'solana' and pair.get('dexId') == 'meteora'
    ]

    # Return only 5 pairs (or all if less than 5 exist)
    return filtered_pairs[:5]


async def create_balanced_pool(token_address: str, amount: float, api_url: str ):
    """
    Creates a balanced liquidity pool by adding the specified token and amount.

    Args:
        token_address (str): The token address to add liquidity for (e.g., USDC)
        amount (float): The amount of tokens to add as liquidity
        api_url (str): The endpoint URL (defaults to localhost)

    Returns:
        dict: Response from the API containing transaction details or error
    """
    payload = {
        "tokenAddress": token_address,
        "amount": amount
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error creating balanced pool: {e}")
        if hasattr(e, 'response') and e.response is not None:
            return e.response.json()
        return {"error": str(e)}
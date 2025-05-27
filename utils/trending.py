import requests
from bs4 import BeautifulSoup
import json


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

# if __name__ == '__main__':
#     pairs = get_solana_meteora_pairs()
    
#     # Print the results in a readable format
#     print(f"Found {len(pairs)} Solana/Meteora pairs:")
#     for i, pair in enumerate(pairs, 1):
#         print(f"\nPair #{i}:")
#         print(f"Token: {pair['baseToken']['name']} ({pair['baseToken']['symbol']})")
#         print(f"Address: {pair['baseToken']['address']}")
#         print(f"Pair Address: {pair['pairAddress']}")
#         print(f"Price (Native): {pair['priceNative']}")
#         print(f"Price (USD): {pair['priceUsd']}")
#         print(f"Transactions (5m): {pair['txns']['m5']['buys']} buys, {pair['txns']['m5']['sells']} sells")
#         print(f"DexScreener URL: {pair['url']}")
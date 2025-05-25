import requests

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
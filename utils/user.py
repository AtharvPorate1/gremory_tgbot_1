import aiohttp
import json



async def check_user_in_db(tgId: str):
    url = f"http://localhost:3000/api/users/verify/{tgId}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()
        

async def get_wallet_address(tgId: str):
    print(f"Fetching wallet address for user {tgId}")
    url = f"http://localhost:3000/api/users/{tgId}/getwallet"
    headers = {
        "Content-Type": "application/json"
    }
    print(f"Requesting wallet address from {url}")
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers ) as response:
            return await response.json()
        

async def create_new_user(tgId: str, username: str):
    print(f"Creating new user with username: {username} and tgId: {tgId}")
    url = "http://localhost:3000/api/users/new-user"
    payload = {
        "username": username,
        "tgId": tgId
    }
    headers = {
        "Content-Type": "application/json"
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers) as response:
                try:
                    resp_json = await response.json()
                except aiohttp.ContentTypeError:
                    resp_json = {"error": "Invalid response format", "status": response.status}
                if response.status != 200:
                    resp_json["error"] = f"Request failed with status {response.status}"
                with open("new_user_response.json", "w") as f:
                    json.dump(resp_json, f, indent=4)
                return resp_json
    except aiohttp.ClientError as e:
        error_resp = {"error": f"HTTP Client error: {str(e)}"}
        with open("new_user_response.json", "w") as f:
            json.dump(error_resp, f, indent=4)
        return error_resp
    except Exception as e:
        error_resp = {"error": f"Unexpected error: {str(e)}"}
        with open("new_user_response.json", "w") as f:
            json.dump(error_resp, f, indent=4)
        return error_resp
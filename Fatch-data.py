import requests
import json

Url = "https://api.freecryptoapi.com/v1/getCryptoList"

headers = {
    "api_key": "gp1fi5g1c1bpgbuw5tdp",
   "Authorization": "Bearer gp1fi5g1c1bpgbuw5tdp"
}

response = requests.get(Url, headers=headers)
if response.status_code == 200:
    data = response.json()
    with open("Crypto_Data.json", "w") as f:
        json.dump(data, f,indent=2)
else:
    print(f"Error: {response.status_code}")

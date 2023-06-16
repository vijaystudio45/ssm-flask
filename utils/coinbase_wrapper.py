# 8bd07453-6fec-489f-ad08-e248ae519ee5

import requests
import pprint


class CoinbaseWrapper:
    def __init__(self, api_key):
        self.api_key = api_key
        self.headers = self._create_headers()

    def _create_headers(self):
        headers = {"Content-Type": "application/json", "X-CC-Api-Key": self.api_key, "X-CC-Version": "2018-03-22"}

        return headers

    def API_create_charge(self, customer_id, customer_name, amount):

        body = {
            "name": customer_name,
            "description": f"Boostgram account balance topup.",
            "pricing_type": "fixed_price",
            "local_price": {"amount": f"{amount}", "currency": "USD"},
            "metadata": {
                "customer_id": customer_id,
            },
            "redirect_url": "https://charge/completed/page",  # To be changed
            "cancel_url": "https://charge/canceled/page",  # To be changed
        }
        print("coinbase headers:", self.headers)
        r = requests.post(url="https://api.commerce.coinbase.com/charges", headers=self.headers, json=body)
        return dict(r.json())

    def API_get_charge(self, charge_id):
        r = requests.get(url=f"https://api.commerce.coinbase.com/charges/{charge_id}", headers=self.headers)
        return dict(r.json())

    def API_get_all_charges(self):
        URL = "https://api.commerce.coinbase.com/charges"
        while True:
            r = requests.get(url=URL, headers=self.headers)
            rjson = dict(r.json()) 
            URL = rjson['pagination']['next_uri']
            for charge in rjson['data']:
                yield charge
            print(URL)
            if URL == None:
                break
        
        return None


import hmac
import hashlib
import time
import requests
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

# === YOUR API KEYS HERE ===
API_KEY = "YOUR_MEXC_API_KEY"
API_SECRET = "YOUR_MEXC_SECRET_KEY"

BASE_URL = "https://api.mexc.com"

def get_server_time():
    return int(time.time() * 1000)

def sign(params):
    query_string = "&".join(["{}={}".format(k, params[k]) for k in sorted(params)])
    return hmac.new(API_SECRET.encode("utf-8"), query_string.encode("utf-8"), hashlib.sha256).hexdigest()

def get_account_balance(asset="USDT"):
    timestamp = get_server_time()
    params = {
        "timestamp": timestamp
    }
    params["signature"] = sign(params)
    headers = {
        "X-MEXC-APIKEY": API_KEY
    }
    response = requests.get(f"{BASE_URL}/api/v3/account", headers=headers, params=params)
    balances = response.json().get("balances", [])
    for b in balances:
        if b["asset"] == asset:
            return float(b["free"])
    return 0.0

def place_market_order(symbol, side, quantity):
    timestamp = get_server_time()
    params = {
        "symbol": symbol,
        "side": side.upper(),
        "type": "MARKET",
        "quantity": quantity,
        "timestamp": timestamp
    }
    params["signature"] = sign(params)
    headers = {
        "X-MEXC-APIKEY": API_KEY
    }
    response = requests.post(f"{BASE_URL}/api/v3/order", headers=headers, params=params)
    return response.json()

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    symbol = data.get("symbol", "ETHUSDT")
    side = data.get("action", "buy").upper()

    # Step 1: Get available USDT balance
    usdt_balance = get_account_balance("USDT")

    # Step 2: Get current price of ETH
    ticker = requests.get(f"{BASE_URL}/api/v3/ticker/price", params={"symbol": symbol}).json()
    price = float(ticker["price"])

    # Step 3: Calculate quantity (max compounding)
    quantity = round(usdt_balance / price, 6)

    # Step 4: Place market order
    result = place_market_order(symbol, side, quantity)

    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

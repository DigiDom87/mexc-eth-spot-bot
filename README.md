# MEXC Spot ETH/USDT Trading Bot

This bot executes live market trades on the MEXC Spot exchange based on webhook alerts from TradingView. It uses full balance compounding and executes trades on the ETH/USDT pair.

## Features
- Connects to MEXC Spot API
- Places market buy/sell orders using all available USDT
- Automatically calculates quantity based on live ETH price
- Accepts webhook alerts via Flask server

## Setup Instructions

1. **Set up Railway environment variables:**
    - `API_KEY` — Your MEXC API Key
    - `API_SECRET` — Your MEXC Secret Key

2. **Webhook format (from TradingView):**
    ```
    {
      "action": "buy",
      "symbol": "ETHUSDT"
    }
    ```

3. **Deploy to Railway:**
    - Upload all files from this repo
    - Railway will use `Procfile` to start Flask server
    - Webhook URL will be:
      ```
      https://<your-railway-app>.up.railway.app/webhook
      ```

4. **Security Tips:**
    - Use IP whitelisting in MEXC API settings if possible
    - Do NOT enable `Withdraw` unless required

## Dependencies
See `requirements.txt`.

## License
MIT

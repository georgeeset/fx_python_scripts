import websocket
import json
import time
import logging

class BinanceWebSocket:
    def __init__(self, symbols):
        self.socket_url = "wss://stream.binance.com:9443/ws"
        self.symbols = symbols
        self.ws = None
        self.subscribe_message = json.dumps({
            "method": "SUBSCRIBE",
            "params": [f"{symbol.lower()}@trade" for symbol in symbols],
            "id": 1
        })

    def on_message(self, ws, message):
        data = json.loads(message)
        if 'p' in data:
            symbol = data['s']
            price = data['p']
            print(f"Symbol: {symbol}, Price: {price}")

    def on_error(self, ws, error):
        logging.error(f"Error: {error}")

    def on_close(self, ws, close_status_code, close_msg):
        logging.warning("Connection closed. Reconnecting...")
        time.sleep(5)
        self.connect()

    def on_open(self, ws):
        logging.info("Connection opened.")
        ws.send(self.subscribe_message)

    def connect(self):
        self.ws = websocket.WebSocketApp(self.socket_url,
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close)
        self.ws.on_open = self.on_open
        self.ws.run_forever()

class TradingBot:
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        self.ws = BinanceWebSocket(symbols=["BTCUSDT", "ETHUSDT"])

    def start(self):
        self.ws.connect()

    def place_margin_order(self, symbol, side, quantity, price):
        # Placeholder for placing margin orders
        pass

    def send_telegram_message(self, message):
        # Placeholder for sending Telegram messages
        pass

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    bot = TradingBot(api_key='your_api_key', api_secret='your_api_secret')
    bot.start()

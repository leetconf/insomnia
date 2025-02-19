import json, threading, time
from websocket import WebSocketApp
from insomnia.utils import ident_data, log
from insomnia.config import TOKEN, USER_AGENT, BROWSER, OS

GATEWAY_URL = "wss://gateway.discord.gg/?v=10&encoding=json"

class Client: 
    def __init__(self):
        self.ws: WebSocketApp = None
        self.heartbeat_interval: int = None
        self.connected: bool = False

    def on_message(self, ws, message):
        data: dict = json.loads(message)
        code = data.get("op") # Status code
        event_name = data.get("t") # Event name
        event_data = data.get("d") # Event data (JSON)

        if code == 10:
            self.heartbeat_interval = event_data['heartbeat_interval'] / 1000
            threading.Thread(target=self.heartbeat, daemon=True).start()
            client_info = {"os": OS, "browser": BROWSER, "user_agent": USER_AGENT}
            ws.send(ident_data(TOKEN, client_info))

        if event_name == "READY":
            print("[READY] Logged in as: {}".format(event_data["user"]["username"]))

        elif event_name == "MESSAGE_CREATE":
            log(event_data)
            
    def on_error(self, _, error):
        print(f"[ERROR] {error}")

    def on_close(self, _, close_status_code, close_msg):
        print(f"[CLOSED] Code: {close_status_code}, Message: {close_msg}")
        self.die()

    def on_open(self, _):
        print("[CONNECTED] WebSocket connection established.")
        self.connected = True

    def heartbeat(self):
        while self.connected:
            payload = {
                "op": 1,
                "d": None
            }
            self.ws.send(json.dumps(payload))
            time.sleep(self.heartbeat_interval)

    def run(self):
        self.ws = WebSocketApp(
            GATEWAY_URL,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
            on_open=self.on_open
        )
        self.ws.run_forever()

    def die(self):
        print("[INFO] Closing connection")
        self.connected = False
        self.ws.close()

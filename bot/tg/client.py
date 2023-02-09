import requests
from marshmallow import ValidationError
import bot
from bot.tg.dc import GetUpdatesResponse, SendMessageResponse


class TgClient:
    def __init__(self, token):
        self.token = token

    def get_url(self, method: str):
        return f"https://api.telegram.org/bot{self.token}/{method}"

    def get_updates(self, offset: int = 0, timeout: int = 60) -> GetUpdatesResponse:
        url = self.get_url("getUpdates")
        resp = requests.get(url, params={"offset": offset, "timeout": timeout})
        try:
            return GetUpdatesResponse.Schema().load(resp.json())
        except ValidationError:
            return GetUpdatesResponse.Schema().load({'ok': True, 'result': []})

    def send_message(self, chat_id: int, text: str) -> SendMessageResponse:
        url = self.get_url("sendMessage")
        resp = requests.post(url, json={"chat_id": chat_id, "text": text})
        return SendMessageResponse.Schema().load(resp.json())


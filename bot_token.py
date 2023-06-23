"""用于储存bot的token和appid"""
import json


BOT_APPID = "{{APPID}}"
TOKEN = "{{TOKEN}}"

with open("database/account.json", "r", encoding="utf-8") as file:
    info = json.loads(file.read())
    BOT_APPID = info["bot_appid"]
    TOKEN = info["token"]

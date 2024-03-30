import os
import sys
import json
import time
import requests
import websocket
from keep_alive import keep_alive

DEVELOPED_BY = "NINJA TEAM"
DISCORD_LINK = "https://discord.gg/STVe3yBABf"

status = "online"
GUILD_ID = input("Enter your server (guild) ID: ")
CHANNEL_ID = input("Enter your channel ID: ")
usertoken = input("Enter your Discord token: ")

SELF_MUTE = True
SELF_DEAF = False
SELF_STREAM = True

headers = {"Authorization": usertoken, "Content-Type": "application/json"}

validate = requests.get('https://canary.discordapp.com/api/v9/users/@me', headers=headers)
if validate.status_code != 200:
    print("[ERROR] Your token might be invalid. Please check it again.")
    sys.exit()

userinfo = requests.get('https://canary.discordapp.com/api/v9/users/@me', headers=headers).json()
username = userinfo["username"]
discriminator = userinfo["discriminator"]
userid = userinfo["id"]

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def joiner(token, status, guild_id, channel_id):
    ws = websocket.WebSocket()
    ws.connect('wss://gateway.discord.gg/?v=9&encoding=json')
    start = json.loads(ws.recv())
    heartbeat = start['d']['heartbeat_interval']
    auth = {
        "op": 2,
        "d": {
            "token": token,
            "properties": {"$os": "Windows 10", "$browser": "Google Chrome", "$device": "Windows"},
            "presence": {"status": status, "afk": False}
        },
        "s": None,
        "t": None
    }
    vc = {
        "op": 4,
        "d": {
            "guild_id": int(guild_id),
            "channel_id": int(channel_id),
            "self_mute": SELF_MUTE,
            "self_deaf": SELF_DEAF
        },
        "self_stream": SELF_STREAM
    }
    ws.send(json.dumps(auth))
    ws.send(json.dumps(vc))
    time.sleep(heartbeat / 1000)
    ws.send(json.dumps({"op": 1, "d": None}))

def run_joiner():
    clear_screen()
    print(f"Logged in as {username}#{discriminator} ({userid}).")
    print(f"Developed by: {DEVELOPED_BY}")
    print(f"Discord: {DISCORD_LINK}")

    while True:
        joiner(usertoken, status, GUILD_ID, CHANNEL_ID)
        time.sleep(30)

keep_alive()
run_joiner()

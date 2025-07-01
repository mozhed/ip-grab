from flask import Flask, request, redirect, session
from datetime import datetime
import requests
import os
import time
from dotenv import load_dotenv

# Load .env
load_dotenv()

app = Flask(__name__)
app.secret_key = "a-super-secret-key"  # For session handling

WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK")

def send_to_discord(ip, user_agent, date, geo_data):
    country = geo_data.get("country", "Unknown")
    city = geo_data.get("city", "Unknown")
    isp = geo_data.get("isp", "Unknown")

    embed = {
        "title": "📡 New Visitor Logged",
        "description": f"**IP**: {ip}\n"
                       f"**Date**: {date}\n"
                       f"**Country/City**: {country}, {city}\n"
                       f"**ISP**: {isp}\n"
                       f"**User Agent**: {user_agent}",
        "color": 3066993
    }

    payload = {
        "content": None,
        "embeds": [embed]
    }

    try:
        requests.post(WEBHOOK_URL, json=payload)
    except Exception as e:
        print("Failed to send to Discord:", e)

@app.before_request
def rate_limit():
    now = time.time()
    if "last_visit" in session and now - session["last_visit"] < 5:
        return "Too many requests. Slow down!", 429
    session["last_visit"] = now

@app.route("/")
def index():
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user_agent = request.headers.get("User-Agent", "Unknown")

    try:
        geo = requests.get(f"http://ip-api.com/json/{ip}").json()
    except:
        geo = {}

    # Log locally
    with open("visits.log", "a") as f:
        f.write(f"{ip} | {date} | {geo.get('country', 'N/A')} | {user_agent}\n")

    # Send to Discord
    send_to_discord(ip, user_agent, date, geo)

    return redirect("https://google.com")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3101)

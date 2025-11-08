import requests

CLIENT_ID = "61fd7975-7ff4-4780-b784-d8e9f1dc23ec"
CLIENT_SECRET = "pr($pIxM0dtzAF(!%*#U?gMrf2w#eWvMs0RI$jUAZV7GH77c#16*I~dHzQs6aWnU"

r = requests.post(
    "https://cloud.uipath.com/identity_/connect/token",
    data={
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    },
    headers={"Content-Type": "application/x-www-form-urlencoded"},
)
print(r.status_code, r.text)

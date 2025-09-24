import requests

url = "https://sso.profitbase.ru/api/oauth2/token"

payload = {
    "client_id": "site_widget",
    "client_secret": "site_widget",
    "grant_type": "site_widget",
    "scope": "SITE_WIDGET",

}

headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "x-tenant-id": "4242",  # ← у тебя этот ID
    "origin": "https://xn--80abdl0adtby.xn--p1ai",
    "referer": "https://xn--80abdl0adtby.xn--p1ai",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
}

resp = requests.post(url, json=payload, headers=headers)
resp.raise_for_status()

token = resp.json().get("access_token")
print("Bearer", token)
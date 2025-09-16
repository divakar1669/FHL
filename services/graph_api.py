import requests
from config import config

def get_access_token():
    url = f"https://login.microsoftonline.com/{config.TENANT_ID}/oauth2/v2.0/token"
    data = {
        "client_id": config.CLIENT_ID,
        "client_secret": config.CLIENT_SECRET,
        "scope": "https://graph.microsoft.com/.default",
        "grant_type": "client_credentials"
    }
    resp = requests.post(url, data=data)
    resp.raise_for_status()
    return resp.json()["access_token"]

def get_post_with_replies(message_id):
    token = get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{config.GRAPH_API_BASE}/teams/{config.TEAM_ID}/channels/{config.CHANNEL_ID}/messages/{message_id}?$expand=replies"
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    return resp.json()

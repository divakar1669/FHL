import requests
import json
from datetime import datetime, timedelta

# === Constants ===
ACCESS_TOKEN = "eyJ0eXAiOiJKV1QiLCJub25jZSI6InJGVndSY0daeUtLQW1uSHlONDRoMC1faVRnUF80N1NrZEtxR3pScW9WVnMiLCJhbGciOiJSUzI1NiIsIng1dCI6IkpZaEFjVFBNWl9MWDZEQmxPV1E3SG4wTmVYRSIsImtpZCI6IkpZaEFjVFBNWl9MWDZEQmxPV1E3SG4wTmVYRSJ9.eyJhdWQiOiIwMDAwMDAwMy0wMDAwLTAwMDAtYzAwMC0wMDAwMDAwMDAwMDAiLCJpc3MiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC83MmY5ODhiZi04NmYxLTQxYWYtOTFhYi0yZDdjZDAxMWRiNDcvIiwiaWF0IjoxNzU4MDg1MjI4LCJuYmYiOjE3NTgwODUyMjgsImV4cCI6MTc1ODA5MDI1MywiYWNjdCI6MCwiYWNyIjoiMSIsImFjcnMiOlsicDEiLCJjMTAiXSwiYWlvIjoiQWJRQVMvOFpBQUFBYUdJbk1YUlhvY09oNVpXb3lHTlUzQnIvMFdkaXEyVlVpbjYwL2IxMVJWWCtBaTdUS2lGdVFwUmtNZE53a1BzSDNETDVEYzZ0aWpjcndnMldTYjh0WE1ScndMdmdoWnRZNEZXbzFlRzJyNElrdnowU3VzYm44Z3g2eDhMazRJNXI5OXVkSlp3U2ZaVS9LeUk4RktSd1hKY0ZmTGo2SWU0Q0VNenBYK3czM25hbHZFSDNQSU9wME9CQWJkSTRWUzJ2bVh5VG8yUjF3aXZld1ErN0gycW1xZEpFeUoxekl2Y0o4UWE2c3ZYd2E1RT0iLCJhbXIiOlsicnNhIiwibWZhIl0sImFwcF9kaXNwbGF5bmFtZSI6IkdyYXBoIEV4cGxvcmVyIiwiYXBwaWQiOiJkZThiYzhiNS1kOWY5LTQ4YjEtYThhZC1iNzQ4ZGE3MjUwNjQiLCJhcHBpZGFjciI6IjAiLCJjYXBvbGlkc19sYXRlYmluZCI6WyIyOTM5OWNmOS05YjZiLTQyMDUtYjViMy0xM2ExMzRlOWIyMzMiXSwiY29udHJvbHMiOlsiYXBwX3JlcyJdLCJjb250cm9sc19hdWRzIjpbImRlOGJjOGI1LWQ5ZjktNDhiMS1hOGFkLWI3NDhkYTcyNTA2NCIsIjAwMDAwMDAzLTAwMDAtMDAwMC1jMDAwLTAwMDAwMDAwMDAwMCIsIjAwMDAwMDAzLTAwMDAtMGZmMS1jZTAwLTAwMDAwMDAwMDAwMCJdLCJkZXZpY2VpZCI6ImNiNjYxNjU5LTZiNzItNGM0My1iYzU3LTM4MWIxMjBhOGFmZiIsImZhbWlseV9uYW1lIjoiVCIsImdpdmVuX25hbWUiOiJEaXZha2FyIiwiaWR0eXAiOiJ1c2VyIiwiaXBhZGRyIjoiMTcyLjE3MS4yMzYuMjQiLCJuYW1lIjoiRGl2YWthciBUIiwib2lkIjoiOWI3ODUyYmEtOTVhOC00YzQyLWE2ZTYtNmJiOGY4MmU0NzA2Iiwib25wcmVtX3NpZCI6IlMtMS01LTIxLTIxMjc1MjExODQtMTYwNDAxMjkyMC0xODg3OTI3NTI3LTc3MjQ1NTgwIiwicGxhdGYiOiIzIiwicHVpZCI6IjEwMDMyMDAzOEExOTUzMDQiLCJyaCI6IjEuQVJvQXY0ajVjdkdHcjBHUnF5MTgwQkhiUndNQUFBQUFBQUFBd0FBQUFBQUFBQUFhQU9jYUFBLiIsInNjcCI6IkNhbGVuZGFycy5SZWFkV3JpdGUgQ29udGFjdHMuUmVhZFdyaXRlIERldmljZU1hbmFnZW1lbnRBcHBzLlJlYWRXcml0ZS5BbGwgRGV2aWNlTWFuYWdlbWVudENvbmZpZ3VyYXRpb24uUmVhZC5BbGwgRGV2aWNlTWFuYWdlbWVudENvbmZpZ3VyYXRpb24uUmVhZFdyaXRlLkFsbCBEZXZpY2VNYW5hZ2VtZW50TWFuYWdlZERldmljZXMuUHJpdmlsZWdlZE9wZXJhdGlvbnMuQWxsIERldmljZU1hbmFnZW1lbnRNYW5hZ2VkRGV2aWNlcy5SZWFkLkFsbCBEZXZpY2VNYW5hZ2VtZW50TWFuYWdlZERldmljZXMuUmVhZFdyaXRlLkFsbCBEZXZpY2VNYW5hZ2VtZW50UkJBQy5SZWFkLkFsbCBEZXZpY2VNYW5hZ2VtZW50UkJBQy5SZWFkV3JpdGUuQWxsIERldmljZU1hbmFnZW1lbnRTZXJ2aWNlQ29uZmlnLlJlYWQuQWxsIERldmljZU1hbmFnZW1lbnRTZXJ2aWNlQ29uZmlnLlJlYWRXcml0ZS5BbGwgRGlyZWN0b3J5LkFjY2Vzc0FzVXNlci5BbGwgRGlyZWN0b3J5LlJlYWRXcml0ZS5BbGwgRmlsZXMuUmVhZFdyaXRlLkFsbCBHcm91cC5SZWFkV3JpdGUuQWxsIElkZW50aXR5Umlza0V2ZW50LlJlYWQuQWxsIE1haWwuUmVhZFdyaXRlIE1haWxib3hTZXR0aW5ncy5SZWFkV3JpdGUgTm90ZXMuUmVhZFdyaXRlLkFsbCBvcGVuaWQgUGVvcGxlLlJlYWQgUG9saWN5LlJlYWQuQWxsIFByZXNlbmNlLlJlYWQgUHJlc2VuY2UuUmVhZC5BbGwgcHJvZmlsZSBSZXBvcnRzLlJlYWQuQWxsIFNpdGVzLlJlYWRXcml0ZS5BbGwgVGFza3MuUmVhZFdyaXRlIFVzZXIuUmVhZCBVc2VyLlJlYWRCYXNpYy5BbGwgVXNlci5SZWFkV3JpdGUgVXNlci5SZWFkV3JpdGUuQWxsIGVtYWlsIiwic2lkIjoiMDA0ZmQ1OTktYjdjNS1kZTM1LTBmZmItNzgwNTI3NTY5ZTBjIiwic2lnbmluX3N0YXRlIjpbImR2Y19tbmdkIiwiZHZjX2NtcCIsImttc2kiXSwic3ViIjoiWTJOQmtrZ1RmNnVZSUNNWWJQMkpEbEdJVlBfcGgwamQyWTNMN3N3bkJlTSIsInRlbmFudF9yZWdpb25fc2NvcGUiOiJXVyIsInRpZCI6IjcyZjk4OGJmLTg2ZjEtNDFhZi05MWFiLTJkN2NkMDExZGI0NyIsInVuaXF1ZV9uYW1lIjoiZGl2YWthcnRAbWljcm9zb2Z0LmNvbSIsInVwbiI6ImRpdmFrYXJ0QG1pY3Jvc29mdC5jb20iLCJ1dGkiOiJwRFVta3ctSUcwdXZycnFZby1NSUFBIiwidmVyIjoiMS4wIiwid2lkcyI6WyJiNzlmYmY0ZC0zZWY5LTQ2ODktODE0My03NmIxOTRlODU1MDkiXSwieG1zX2NjIjpbIkNQMSJdLCJ4bXNfZnRkIjoicTdtOFBxNTVzVHpYY2RWQlRqQ2U2TlowX0VUS0dlOWVtcGh4SWg4TE5ab0JhMjl5WldGalpXNTBjbUZzTFdSemJYTSIsInhtc19pZHJlbCI6IjIyIDEiLCJ4bXNfc3NtIjoiMSIsInhtc19zdCI6eyJzdWIiOiJmc0lVWFZLU0N2ajRKRDlWcnpxamhMS2V4VlNuYzJ0VHRxLTlOX3JucUdFIn0sInhtc190Y2R0IjoxMjg5MjQxNTQ3fQ.SJL4ZH2we7EXa3AS3WVhJtBsahy-UWdK7UZzVXX-CRHMqZqtiq5oI6-Aa_UdJM9KjXP5GsfMTTQEzUIUgW3niNuHDSGvrbzt9x3LFCISVntlyGPbT7giTNk4cfamj8LvGcy2w_7qxvum-F95OJa8qGNkXpMO6HWDwvMMhxNpcWwh_Ik-hx9xDNwq5gLRn_M7543oanQyDG0xEf-Yz0dgnF9G8KArz7LRN_5NIQjrocK9cmOfb7uVM5IeRcGA519n6zlk-83dlOwX4g6kI8OnWvoyaCRBLlG6ALQdysZZ8NXSOXGgQNTiDHE_qj4BD8q1n1FTq3PrD1VKiuVrjrCQtQ"  # keep constant, fetch with SP or delegated auth
TEAM_ID = "4026aab5-5f82-4e6b-baac-324d6275db35"
CHANNEL_ID = "19:d5da29dc904643dfac9500d868c7df49@thread.tacv2"
GRAPH_URL = "https://graph.microsoft.com/beta"


headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

def get_paginated_results(url):
    """Fetch paginated results from Graph API."""
    results = []
    while url:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print("Error fetching:", response.text)
            break
        data = response.json()
        results.extend(data.get("value", []))
        url = data.get("@odata.nextLink")
    return results

def get_replies(message_id):
    """Fetch replies for a given message."""
    url = f"{GRAPH_URL}/teams/{TEAM_ID}/channels/{CHANNEL_ID}/messages/{message_id}/replies"
    return get_paginated_results(url)

def build_message_url(message_id):
    """Build Teams message deep link."""
    return f"https://teams.microsoft.com/l/message/{CHANNEL_ID}/{message_id}"

def fetch_posts_with_replies():
    """Fetch posts + replies, filter by date, build JSON structure."""
    url = f"{GRAPH_URL}/teams/{TEAM_ID}/channels/{CHANNEL_ID}/messages"
    posts = get_paginated_results(url)

    structured_data = []

    for post in posts:
        created_time = datetime.fromisoformat(post["createdDateTime"].replace("Z", "+00:00"))
        if created_time < one_month_ago:  # skip old posts
            continue

        post_obj = {
            "post": {
                "id": post["id"],
                "author": post.get("from", {}).get("user", {}).get("displayName", "Unknown"),
                "dateTime": post["createdDateTime"],
                "content": post.get("body", {}).get("content", "").strip(),
                "url": build_message_url(post["id"])
            },
            "replies": []
        }

        replies = get_replies(post["id"])
        for reply in replies:
            reply_obj = {
                "id": reply["id"],
                "author": reply.get("from", {}).get("user", {}).get("displayName", "Unknown"),
                "dateTime": reply["createdDateTime"],
                "content": reply.get("body", {}).get("content", "").strip()
            }
            post_obj["replies"].append(reply_obj)

        structured_data.append(post_obj)

    return structured_data


# === Date filter: last 1 month ===
one_month_ago = datetime.utcnow() - timedelta(days=5)

data = fetch_posts_with_replies()
    
with open("teams_threads.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"✅ Saved {len(data)} posts (with replies) from last 5 days to teams_threads.json")

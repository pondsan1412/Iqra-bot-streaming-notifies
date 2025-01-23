import requests
import json

class TwitchAPI:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = "https://api.twitch.tv/helix"
        self.token = self.get_access_token()

    def get_access_token(self):
        url = "https://id.twitch.tv/oauth2/token"
        params = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials",
        }
        r = requests.post(url, params=params)
        r.raise_for_status()
        return r.json()["access_token"]

    def get_user(self, username):
        url = f"{self.base_url}/users"
        params = {"login": username}
        headers = {
            "Client-ID": self.client_id,
            "Authorization": f"Bearer {self.token}",
        }
        r = requests.get(url, headers=headers, params=params)
        r.raise_for_status()
        return r.json()["data"]

    def get_followers(self, user_id):
        url = f"{self.base_url}/users/follows"
        params = {"to_id": user_id}
        headers = {
            "Client-ID": self.client_id,
            "Authorization": f"Bearer {self.token}",
        }
        r = requests.get(url, headers=headers, params=params)
        if r.status_code == 410:
            raise Exception("This endpoint is no longer supported by Twitch API.")
        r.raise_for_status()
        return r.json()


    def get_clips(self, broadcaster_id):
        url = f"{self.base_url}/clips"
        params = {"broadcaster_id": broadcaster_id}
        headers = {
            "Client-ID": self.client_id,
            "Authorization": f"Bearer {self.token}",
        }
        r = requests.get(url, headers=headers, params=params)
        r.raise_for_status()
        return r.json()

    def check_live_status(self, user_id):
        url = f"{self.base_url}/streams"
        params = {"user_id": user_id}
        headers = {
            "Client-ID": self.client_id,
            "Authorization": f"Bearer {self.token}",
        }
        r = requests.get(url, headers=headers, params=params)
        r.raise_for_status()
        return r.json()["data"]

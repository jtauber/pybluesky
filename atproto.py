import requests


class Agent:
    def __init__(self, url_path="https://bsky.social/xrpc/"):
        self.url_path = url_path
        self.accessJwt = None

    def headers(self):
        if self.accessJwt:
            return {"Authorization": f"Bearer {self.accessJwt}"}
        else:
            return {}

    def get(self, method, **params):
        r = requests.get(self.url_path + method, headers=self.headers(), params=params)
        if r.status_code != 200:
            raise Exception(r.json())
        else:
            return r.json()

    def post(self, method, payload):
        r = requests.post(self.url_path + method, headers=self.headers(), json=payload)
        if r.status_code != 200:
            raise Exception(r.json())
        else:
            return r.json()

    def login(self, identifier, password):
        r = self.post("com.atproto.server.createSession", {"identifier": identifier, "password": password})
        self.accessJwt = r["accessJwt"]
        return r

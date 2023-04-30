#!/usr/bin/env python3

# quick demo script to post

# I might eventually make this doable from the CLI

import datetime
import os
import pprint

from dotenv import load_dotenv

from atproto import Agent

load_dotenv()

IDENTIFIER = os.environ.get("BLUESKY_IDENTIFIER")
PASSWORD = os.environ.get("BLUESKY_PASSWORD")

def display(result):
    pprint.pprint(result, sort_dicts=False)


ag = Agent()
ag.login(IDENTIFIER, PASSWORD)

me = ag.get("com.atproto.identity.resolveHandle", handle=IDENTIFIER)["did"]

display(ag.post("com.atproto.repo.createRecord", {
    "repo": me,
    "collection": "app.bsky.feed.post",
    "record": {
        "$type": "app.bsky.feed.post",
        "text": "Hello Bluesky!",
        "createdAt": datetime.datetime.utcnow().isoformat(),
    }
}))

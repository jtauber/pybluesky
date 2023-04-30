#!/usr/bin/env python3

# quick demo script to get a list of your followers

# I might eventually make this doable from the CLI

import os

from dotenv import load_dotenv

from atproto import Agent

load_dotenv()

IDENTIFIER = os.environ.get("BLUESKY_IDENTIFIER")
PASSWORD = os.environ.get("BLUESKY_PASSWORD")

ag = Agent()

ag.login(IDENTIFIER, PASSWORD)
me = ag.get("com.atproto.identity.resolveHandle", handle="jtauber.com")["did"]

result = ag.get("app.bsky.graph.getFollowers", actor=me)
while True:
    for follow in result["followers"]:
        print(follow.get("displayName"), follow.get("handle"), sep="\t")
    if result.get("cursor") is None:
        break
    result = ag.get("app.bsky.graph.getFollowers", actor=me, cursor=result["cursor"])

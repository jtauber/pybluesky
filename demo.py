#!/usr/bin/env python3

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

display(ag.get("com.atproto.server.describeServer"))

ag.login(IDENTIFIER, PASSWORD)
me = ag.get("com.atproto.identity.resolveHandle", handle="jtauber.com")["did"]
display(ag.get("app.bsky.actor.getProfile", actor=me))


result = ag.get("app.bsky.graph.getFollows", actor=me)
while True:
    for follow in result["follows"]:
        print(follow.get("displayName"), follow.get("handle"))
    if result.get("cursor") is None:
        break
    result = ag.get("app.bsky.graph.getFollows", actor=me, cursor=result["cursor"])

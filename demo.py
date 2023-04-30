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


result = ag.get("app.bsky.graph.getFollowers", actor=me)
while True:
    for follow in result["followers"]:
        print(follow.get("displayName"), follow.get("handle"), follow.get("viewer"))
    if result.get("cursor") is None:
        break
    result = ag.get("app.bsky.graph.getFollowers", actor=me, cursor=result["cursor"])


ag.get("com.atproto.repo.describeRepo", repo=me)
ag.get("com.atproto.repo.listRecords", repo=me, collection="app.bsky.feed.post")
ag.get(
    "com.atproto.repo.getRecord",
    repo=me,
    collection="app.bsky.feed.post",
    rkey="3jtubanyq5y2w",
)

# at://did:plc:cvmmvawq5z2qxfhtu3umrx3f/app.bsky.graph.follow/3ju6ejrzybx22

display(
    ag.get(
        "com.atproto.repo.getRecord",
        repo=me,
        collection="app.bsky.graph.follow",
        rkey="3ju6ejrzybx22",
    )
)

display(ag.get("com.atproto.server.getAccountInviteCodes"))



# at://did:plc:cvmmvawq5z2qxfhtu3umrx3f/app.bsky.feed.post/3juhpcbbgjq2f

print()

display(
    ag.get(
        "app.bsky.feed.getPosts",
        uris=["at://did:plc:cvmmvawq5z2qxfhtu3umrx3f/app.bsky.feed.post/3jtubanyq5y2w"],
    )
)

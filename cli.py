#!/usr/bin/env python3

import os
import pprint

import typer
import dotenv

from atproto import Agent


def display(result):
    pprint.pprint(result, sort_dicts=False)


dotenv.load_dotenv()

IDENTIFIER = os.environ.get("BLUESKY_IDENTIFIER")
PASSWORD = os.environ.get("BLUESKY_PASSWORD")


app = typer.Typer()


ag = Agent()

## eventually this can be generated from lexicon files

@app.command()
def describe_server():
    display(ag.get("com.atproto.server.describeServer"))

@app.command()
def get_account_invite_codes():
    ag.login(IDENTIFIER, PASSWORD)
    display(ag.get("com.atproto.server.getAccountInviteCodes"))

@app.command()
def resolve_handle(handle: str):
    ag.login(IDENTIFIER, PASSWORD)
    display(ag.get("com.atproto.identity.resolveHandle", handle=handle))

@app.command()
def get_profile(actor: str):
    ag.login(IDENTIFIER, PASSWORD)
    display(ag.get("app.bsky.actor.getProfile", actor=actor))

@app.command()
def get_follows(actor: str, cursor: str = None):
    ag.login(IDENTIFIER, PASSWORD)
    if cursor is None:
        display(ag.get("app.bsky.graph.getFollows", actor=actor))
    else:
        display(ag.get("app.bsky.graph.getFollows", actor=actor, cursor=cursor))

@app.command()
def get_followers(actor: str, cursor: str = None):
    ag.login(IDENTIFIER, PASSWORD)
    if cursor is None:
        display(ag.get("app.bsky.graph.getFollowers", actor=actor))
    else:
        display(ag.get("app.bsky.graph.getFollowers", actor=actor, cursor=cursor))

@app.command()
def describe_repo(repo: str):
    ag.login(IDENTIFIER, PASSWORD)
    display(ag.get("com.atproto.repo.describeRepo", repo=repo))

@app.command()
def list_records(repo: str, collection: str, cursor: str = None):
    ag.login(IDENTIFIER, PASSWORD)
    if cursor is None:
        display(ag.get("com.atproto.repo.listRecords", repo=repo, collection=collection))
    else:
        display(ag.get("com.atproto.repo.listRecords", repo=repo, collection=collection, cursor=cursor))

@app.command()
def get_record(repo: str, collection: str, rkey: str):
    ag.login(IDENTIFIER, PASSWORD)
    display(ag.get("com.atproto.repo.getRecord", repo=repo, collection=collection, rkey=rkey))


if __name__ == "__main__":
    app()

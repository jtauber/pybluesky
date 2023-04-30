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


if __name__ == "__main__":
    app()

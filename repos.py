#!/usr/bin/env python3

from atproto import Agent

ag = Agent()



def _display(result):
    for repo in result["repos"]:
        print(repo.get("did"), repo.get("head"), sep="\t")


ag.page(_display, "com.atproto.sync.listRepos", limit=1000)

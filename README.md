# AT Protocol implementation in Python

This is _just_ starting, as I begin to grok Bluesky and the AT Protocol.
I'm releasing it super early for educational purposes only.

Set environment variables `BLUESKY_IDENTIFIER` and `BLUESKY_PASSWORD` to run `demo.py`.
The password should be an **App Password**, not your main password.

- `atproto.py` basic client library for accessing the Bluesky PDS.
- `utils.py` basic util functions
- `lexicon.py` work-in-progress module for dealing with lexicon files

- `demo.py` runnable script trying things out
- `cli.py` command-line interface
- `followers.py` quick script to list your followers (display name and handle)
- `post.py` quick script to post
- `repos.py` quick script to list repos


## What I've Tried

### com.atproto.admin

Nothing yet.

### com.atproto.identity

* resolveHandle

### com.atproto.label

Nothing yet.

### com.atproto.moderation

Nothing yet.

### com.atproto.repo

* describeRepo
* listRecords
* getRecord
* createRecord

### com.atproto.server

* describeServer
* createSession
* getAccountInviteCodes
* getSession

### com.atproto.sync

* listRepos

### app.bsky.actor

* getProfile

### app.bsky.embed

Nothing yet.

### app.bsky.feed

* getPosts

Collections:

* post

### app.bsky.graph

* getFollows
* getFollowers

Collections:

* follow

### app.bsky.notification

Nothing yet.

### app.bsky.richtext

Nothing yet.


## Changes to API since I first started

- new method `app.bsky.feed.getPosts`
- `app.bsky.embed.record` now included `labels`

- `viewerState` in `app.bsky.actor.defs` now has extra properties `blockedBy` (boolean) and `blocking` (at-uri)
- `app.bsky.embed.record` allows for embedded records to reference posts as blocked
- `app.bsky.feed.getAuthorFeed` can return a `BlockedActor` or `BlockedByActor` error
- `app.bsky.feed.getPostThread` allows for a reference to a blocked post and (via change to `app.bsky.feed.defs`) `parent` and `replies` can also reference blocked posts
- there is a new record `app.bsky.graph.block` for blocks with `subject` (did) and `createdAt` (datetime) properties
- new method `app.bsky.graph.getBlocks` that returns who you are blocking (as an array of `profileView`s)

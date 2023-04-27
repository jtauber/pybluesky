def parse_nsid(nsid):
    parts = nsid.split(".")
    name = parts[-1]
    authority = ".".join(parts[1::-1])
    return name, authority


def parse_at_uri(at_uri):
    assert at_uri.startswith("at://")
    repo, collection, record = (at_uri.split("#")[0][5:].split("/") + [None, None])[:3]
    return repo, collection, record
    # fragments not supported yet


if __name__ == "__main__":
    assert parse_nsid("com.example.status") == ("status", "example.com")
    assert parse_at_uri("at://alice.host.com") == ("alice.host.com", None, None)
    assert parse_at_uri("at://did:plc:bv6ggog3tya2z3vxsub7hnal") == ("did:plc:bv6ggog3tya2z3vxsub7hnal", None, None)
    assert parse_at_uri("at://alice.host.com/io.example.song") == ("alice.host.com", "io.example.song", None)
    assert parse_at_uri("at://alice.host.com/io.example.song/3yI5-c1z-cc2p-1a") == ("alice.host.com", "io.example.song", "3yI5-c1z-cc2p-1a")

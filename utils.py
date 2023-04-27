def parse_nsid(nsid):
    parts = nsid.split(".")
    name = parts[-1]
    authority = ".".join(parts[1::-1])
    return name, authority


if __name__ == "__main__":
    assert parse_nsid("com.example.status") == ("status", "example.com")

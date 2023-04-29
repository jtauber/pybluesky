import json


class Lexicon:
    def __init__(self, filename):
        lexicon = json.load(open(filename))
        assert lexicon["lexicon"] == 1
        self.id = lexicon["id"]

        self.defs = {}
        for key, value in lexicon["defs"].items():
            self.defs[key] = {
                defn.my_type: defn
                for defn in [
                    Object,
                    Procedure,
                    Query,
                    Record,
                    String,
                    Subscription,
                    Token,
                ]
            }[value["type"]](value)


class Node:
    def __init__(self, value):
        if set(value.keys()) not in self.properties:
            raise Exception(
                f"{value.keys()} not in {self.properties} in {self.my_type}"
            )
        assert set(value.keys()) in self.properties
        for key, value2 in value.items():
            getattr(self, f"process_{key}")(value2)

    def process_type(self, value):
        if self.my_type != value:
            raise Exception(f"{self.my_type} != {value} in {self}")

    def process_description(self, value):
        assert type(value) == str
        self.description = value

    def process_parameters(self, value):
        self.parameters = Params(value)

    def process_output(self, value):
        self.output = Output(value)

    def process_errors(self, value):
        self.errors = [Error(error) for error in value]

    def process_required(self, value):
        assert type(value) == list
        assert all(type(item) == str for item in value)
        self.required = value  # @@@ validate that these are properties

    def process_properties(self, value):
        self.properties = {}
        for key, value2 in value.items():
            self.properties[key] = {
                prop.my_type: prop
                for prop in [
                    Array,
                    Blob,
                    Boolean,
                    Bytes,
                    CIDLink,
                    Integer,
                    Ref,
                    String,
                    Union,
                    Unknown,
                ]
            }[value2["type"]](value2)

    def process_maxLength(self, value):
        assert type(value) == int
        self.maxLength = value


class Query(Node):
    my_type = "query"
    properties = [
        {"type", "description", "output", "errors"},
        {"type", "description", "output"},
        {"type", "description", "parameters", "output", "errors"},
        {"type", "description", "parameters", "output"},
        {"type", "description", "parameters"},
        {"type", "parameters", "output", "errors"},
        {"type", "parameters", "output"},
    ]


class Procedure(Node):
    my_type = "procedure"
    properties = [
        {"type", "description", "input", "errors"},
        {"type", "description", "input", "output", "errors"},
        {"type", "description", "input", "output"},
        {"type", "description", "input"},
        {"type", "description", "output", "errors"},
        {"type", "description"},
    ]

    def process_input(self, value):
        self.input = Input(value)


class Object(Node):
    my_type = "object"
    properties = [
        {"type", "properties"},
        {"type", "required", "properties"},
        {"type", "required", "nullable", "properties"},
        {"type", "ref"},
        {"type", "description", "required", "properties"},
    ]

    def process_nullable(self, value):
        assert type(value) == list
        self.nullable = value  # @@@ validate that these are properties


class Params(Node):
    my_type = "params"
    properties = [
        {"type", "properties"},
        {"type", "required", "properties"},
    ]


class Output(Node):
    my_type = "(output)"
    properties = [
        {"encoding"},
        {"encoding", "schema"},
    ]

    def process_encoding(self, value):
        assert value in ["application/json", "*/*", "application/vnd.ipld.car"], value
        self.encoding = value

    def process_schema(self, value):
        self.schema = {
            prop.my_type: prop
            for prop in [
                Object,
                Ref,
            ]
        }[
            value["type"]
        ](value)


class Input(Node):
    my_type = "(input)"
    properties = [
        {"encoding"},
        {"encoding", "schema"},
    ]

    def process_encoding(self, value):
        assert value in ["application/json", "*/*", "application/vnd.ipld.car"], value
        self.encoding = value

    def process_schema(self, value):
        self.schema = {
            prop.my_type: prop
            for prop in [
                Object,
            ]
        }[
            value["type"]
        ](value)


class Unknown(Node):
    my_type = "unknown"
    properties = [
        {"type"},
        {"type", "description"},
    ]


class Token(Node):
    my_type = "token"
    properties = [{"type", "description"}]


class Boolean(Node):
    my_type = "boolean"
    properties = [
        {"type"},
        {"type", "description"},
        {"type", "default"},
        {"type", "default", "description"},
        {"type", "const"},
    ]

    def process_const(self, value):
        assert type(value) == bool
        self.const = value

    def process_default(self, value):
        assert type(value) == bool
        self.default = value


class Integer(Node):
    my_type = "integer"
    properties = [
        {"type"},
        {"type", "description"},
        {"type", "default"},
        {"type", "minimum"},
        {"type", "minimum", "maximum", "default"},
        {"type", "minimum", "maximum", "default", "description"},
    ]

    def process_default(self, value):
        assert type(value) == int
        self.default = value

    def process_minimum(self, value):
        assert type(value) == int
        self.default = value

    def process_maximum(self, value):
        assert type(value) == int
        self.default = value


class String(Node):
    my_type = "string"
    properties = [
        {"type"},
        {"type", "format"},
        {"type", "knownValues"},
        {"type", "knownValues", "default"},
        {"type", "description"},
        {"type", "description", "format"},
        {"type", "description", "knownValues"},
        {"type", "description", "maxLength"},
        {"type", "maxGraphemes", "maxLength"},
    ]

    def process_format(self, value):
        assert value in [
            "did",
            "datetime",
            "handle",
            "at-uri",
            "cid",
            "at-identifier",
            "uri",
            "nsid",
        ], value
        self.format = value

    def process_knownValues(self, value):
        assert type(value) == list
        assert all(type(item) == str for item in value)
        self.knowValues = value

    def process_default(self, value):
        assert type(value) == str
        self.default = value

    def process_maxGraphemes(self, value):
        assert type(value) == int
        self.maxLength = value


class Array(Node):
    my_type = "array"
    properties = [
        {"type", "items"},
        {"type", "items", "description"},
        {"type", "items", "maxLength"},
    ]

    def process_items(self, value):
        self.items = {
            prop.my_type: prop
            for prop in [
                CIDLink,
                Integer,
                Ref,
                String,
                Union,
                Unknown,
            ]
        }[value["type"]](value)


class Union(Node):
    my_type = "union"
    properties = [
        {"type", "refs"},
        {"type", "refs", "closed"},
    ]

    def process_refs(self, value):
        assert type(value) == list
        assert all(type(item) == str for item in value)
        self.refs = value

    def process_closed(self, value):
        assert type(value) == bool
        self.closed = value


class Ref(Node):
    my_type = "ref"
    properties = [{"type", "ref"}]

    def process_ref(self, value):
        assert type(value) == str
        self.ref = value


class Subscription(Node):
    my_type = "subscription"
    properties = [
        {"type", "description", "parameters", "message", "errors"},
    ]

    def process_message(self, value):
        self.message = Message(value)


class Blob(Node):
    my_type = "blob"
    properties = [
        {"type"},
        {"type", "accept", "maxSize"},
    ]

    def process_accept(self, value):
        assert value in [
            ["image/*"],
            ["image/png", "image/jpeg"],
        ], value
        self.accept = value

    def process_maxSize(self, value):
        assert type(value) == int
        self.maxSize = value


class CIDLink(Node):
    my_type = "cid-link"
    properties = [{"type"}]


class Bytes(Node):
    my_type = "bytes"
    properties = [{"type", "description", "maxLength"}]


class Record(Node):
    my_type = "record"
    properties = [
        {"type", "key", "record"},
        {"type", "description", "key", "record"},
    ]

    def process_key(self, value):
        assert type(value) == str
        self.key = value

    def process_record(self, value):
        self.record = {
            prop.my_type: prop
            for prop in [
                Object,
            ]
        }[
            value["type"]
        ](value)


class Error(Node):
    my_type = "(error)"
    properties = [{"name"}]

    def process_name(self, value):
        assert type(value) == str
        self.name = value


class Message(Node):
    my_type = "(message)"
    properties = [{"schema"}]

    def process_schema(self, value):
        self.schema = {
            prop.my_type: prop
            for prop in [
                Union,
            ]
        }[
            value["type"]
        ](value)


if __name__ == "__main__":
    import glob

    for filename in sorted(glob.glob("lexicons/com/atproto/*/*.json")):
        # print(f"Loading {filename}")
        Lexicon(filename)

    for filename in sorted(glob.glob("lexicons/app/bsky/*/*.json")):
        # print(f"Loading {filename}")
        Lexicon(filename)

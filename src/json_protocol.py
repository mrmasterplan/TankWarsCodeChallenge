import json


class JSONProtocol:
    def __init__(self):
        self.buffer = ""

    def encode(self, obj):
        """ Encode an object as a JSON string with a newline as a delimiter. """
        return (json.dumps(obj, default=lambda o: o.__dict__) + "\n").encode()

    def decode(self, data):
        """ Decode a byte string into an object. """
        self.buffer += data.decode()

        if "\n" in self.buffer:
            message, self.buffer = self.buffer.split("\n", 1)
            return json.loads(message)
        return None



import json


class JSONProtocol:
    def __init__(self):
        self.buffer = ""

    def encode(self, obj):
        """ Encode an object as a JSON string with a newline as a delimiter. """
        return (json.dumps(obj, default=lambda o: o.__dict__) + "\n").encode()

    def decode(self, data):
        """ Decode a byte string into objects. """
        self.buffer += data.decode()

        ret = []
        while "\n" in self.buffer:
            message, self.buffer = self.buffer.split("\n", 1)
            ret.append( json.loads(message) )
        return ret


class _testObject:
    def __init__(self, ii, aa, ll):
        self.ii = ii
        self.aa = aa
        self.ll = ll

    def __eq__(self, other):
        return self.ii == other.ii and self.aa == other.aa and self.ll == other.ll


if __name__ == "__main__":
    print("Local test")
    jp = JSONProtocol()
    enc = jp.encode(_testObject(1,"aa", [3,4]))

    assert [] == jp.decode(enc[:4])
    nn = jp.decode(enc[4:])
    assert len(nn) == 1
    res = nn[0]
    
    assert _testObject(1,"aa", [3,4]) == _testObject(**res)
    
    enc += jp.encode(_testObject(2,"aa", [3,4]))
    
    out = jp.decode(enc) ##
    
    assert len(out) == 2
    
    assert _testObject(**out[1]).ii == 2
    print("PASSED")

    
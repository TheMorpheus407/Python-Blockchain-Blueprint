import hashlib, codecs

def hash(string):
    sha = hashlib.sha3_256()
    sha.update(string.encode("utf-8"))
    return codecs.encode(sha.digest(), "base64").decode()

def string_to_hex(string):
    return codecs.encode(string.encode("utf-8"), "hex_codec").decode()


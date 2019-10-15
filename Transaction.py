from UTXO import UTXO
import hashing, json
import crypto

class Transaction:
    def __init__(self, utxos, receiver_public_keys, messages, signature):
        assert isinstance(receiver_public_keys, list)
        assert isinstance(messages, list)
        assert len(receiver_public_keys) == len(messages)
        assert len(receiver_public_keys) > 0
        assert (utxos, list)
        assert len(utxos) > 0
        for i in utxos:
            assert isinstance(i, UTXO)
            assert i.public_key == utxos[0].public_key

        self.utxos = utxos
        self.receiver_public_keys = receiver_public_keys
        self.messages = messages
        self.signature = signature

        assert self.is_valid()

    def get_dict(self):
        utxos_json = []
        for i in self.utxos:
            utxos_json.append(i.get_dict())
        return {
            "utxos": utxos_json,
            "receiver_public_keys": self.receiver_public_keys,
            "messages": self.messages
        }

    def get_json(self):
        return json.dumps(self.get_dict())

    def get_hash(self):
        return hashing.hash(self.get_json())

    def get_full_json(self):
        dictionary = self.get_dict()
        dictionary.update({"signature": self.signature})
        return json.dumps(dictionary)

    def is_valid(self):
        signature_valid = crypto.verify(self.utxos[0].public_key, self.signature, self.get_hash())
        spent = 0
        for msg in self.messages:
            spent = spent + msg
        balance = 0
        for utxo in self.utxos:
            balance = balance + utxo.message
        amount_enough = balance == spent
        return signature_valid and amount_enough

class UnsignedTransaction:
    def __init__(self, utxos, receiver_public_keys, messages):
        assert isinstance(receiver_public_keys, list)
        assert isinstance(messages, list)
        assert len(receiver_public_keys) == len(messages)
        assert len(receiver_public_keys) > 0
        assert (utxos, list)
        assert len(utxos) > 0
        for i in utxos:
            assert isinstance(i, UTXO)
            assert i.public_key == utxos[0].public_key

        self.utxos = utxos
        self.receiver_public_keys = receiver_public_keys
        self.messages = messages

    def get_dict(self):
        utxos_json = []
        for i in self.utxos:
            utxos_json.append(i.get_dict())
        return {
            "utxos": utxos_json,
            "receiver_public_keys": self.receiver_public_keys,
            "messages": self.messages
        }

    def get_json(self):
        return json.dumps(self.get_dict())

    def get_hash(self):
        return hashing.hash(self.get_json())

    def sign(self, priv_key, password):
        return crypto.sign(priv_key, password, self.get_hash())

class Coinbase:
    def __init__(self, receiver):
        self.receiver_public_keys = [receiver]
        self.messages = [50]

    def get_hash(self):
        return hashing.hash(self.get_json())

    def is_valid(self):
        return True

    def get_dict(self):
        return {
            "receiver_public_keys": self.receiver_public_keys,
            "messages": self.messages
        }
    
    def get_json(self):
        return json.dumps(self.get_dict())
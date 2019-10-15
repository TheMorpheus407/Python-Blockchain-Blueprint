from Block import Block
from Genesis import genesis_coinbase
from Transaction import Transaction
import hashing
from CONFIG import mining_target
from UTXO import UTXO
import json


the_blockchain = None
def get_blockchain():
    global the_blockchain
    if the_blockchain == None:
        the_blockchain = Blockchain()
    return the_blockchain

#Block1 --> Block2 --> Block3
class Blockchain:
    def __init__(self):
        self.blocks = [Block("WGKu6bQVONnhrWKY0aT3Dl/YbS49An4i49jfMTvLGVY=", [genesis_coinbase()], 0)]

    def insert_block(self, block):
        #TODO check if only one coinbase!
        if not isinstance(block, Block):
            return False
        for tx in block.transactions:
            if not tx.is_valid():
                return False
            if isinstance(tx, Transaction):
                for utxo in tx.utxos:
                    if not self.is_valid_UTXO(utxo):
                        return False
        if not self.check_against_target(block.get_hash()):
            return False
        self.blocks.append(block)
        return True

    def check_against_target(self, hash_string):
        hex = hashing.string_to_hex(hash_string) #"0abdefdeadbeeffaceb00c"
        for i in range(1, mining_target+1):
            if not hex[i] == "0":
                return False
        return True

    def get_utxos(self, public_key):
        utxos = []
        for block in self.blocks:
            for tx in block.transactions:
                counter = 0
                for pk in tx.receiver_public_keys:
                    if pk in public_key:
                        utxo = UTXO(tx.get_hash(), public_key, tx.messages[counter])
                        utxos.append(utxo)
                    counter = counter + 1
        return utxos

    def get_topmost_block(self):
        return self.blocks[len(self.blocks)-1]

    def is_valid_UTXO(self, UTXO):
        valid = False
        for block in self.blocks:
            for tx in block.transactions:
                if tx.get_hash() == UTXO.tx_hash:
                    counter = 0
                    for pk in tx.receiver_public_keys:
                        if pk in UTXO.public_key:
                            if UTXO.message == tx.messages[counter]:
                                valid = True
                        counter = counter + 1
        if valid == False:
            return False

        #check double spending
        for block in self.blocks:
            for tx in block.transactions:
                if isinstance(tx, Transaction):
                    for tx_utxo in tx.utxos:
                        if tx_utxo.get_hash() == UTXO.get_hash():
                            return False
        return True

    # {"blocks":[...]}
    def get_json(self):
        blocks = []
        for i in self.blocks:
            blocks.append(i.get_dict())
        return json.dumps({
            "blocks": blocks
        })

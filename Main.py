import hashing
from Wallet import Wallet
from Blockchain import get_blockchain
from Miner import Miner

if __name__ == "__main__":
    print(hashing.hash("Jetzt liken und abonnieren!!! The Morpheus Tutorials :)"))
    w = Wallet()
    print(w.public_key)
    print(w.private_key)
    print(w.password)
    print(w.send_money([w.public_key], [50]))
    print(get_blockchain().get_json())
    miner = Miner(own_public_key=w.public_key)

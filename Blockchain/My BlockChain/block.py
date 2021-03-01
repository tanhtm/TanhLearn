# coding:utf-8
import hashlib
import time
from model import Model
from database import BlockChainDB

class Block(Model):

    def __init__(self, index, timestamp, tx, merkle, previous_hash, difficulty):
        self.index = index
        self.timestamp = timestamp
        self.tx = tx
        self.merkle= merkle
        self.previous_block = previous_hash
        self.difficulty= difficulty

    def header_hash(self):
        """
        Refer to bitcoin block header hash
        """          
        return hashlib.sha256((str(self.index) + str(self.timestamp) + str(self.tx) + str(self.previous_block)).encode('utf-8')).hexdigest()

    def pow(self):
        """
        Proof of work. Add nonce to block.
        """        
        nonce = 0
        while self.valid(nonce) is False:
            print(nonce)
            nonce += 1
        self.nonce = nonce
        return nonce

    def make(self, nonce):
        """
        Block hash generate. Add hash to block.
        """
        self.hash = self.ghash(nonce)
    
    def ghash(self, nonce):
        """
        Block hash generate.
        """        
        header_hash = self.header_hash()
        token = ''.join((header_hash, str(nonce))).encode('utf-8')
        return hashlib.sha256(token).hexdigest()

    def valid(self, nonce, diff= 4):
        """
        Validates the Proof
        """
        return self.ghash(nonce)[:diff] == "0000"

    def to_dict(self):
        return self.__dict__

def fromDict(bdict):
    b = Block(bdict['index'], bdict['timestamp'], bdict['tx'], bdict['merkle'], 
              bdict['previous_block'], bdict['difficulty']) #######
    b.hash = bdict['hash']
    b.nonce = bdict['nonce']
    return b

def save(block):
    bdb= BlockChainDB()
    bdb.insert(block.to_dict())
        
def getLastBlock():
    bdb= BlockChainDB()
    blocks= bdb.read()
    if len(blocks) > 0:
        return fromDict(blocks[-1])
    return None

def getBlocks():
    bdb= BlockChainDB()
    blocks= bdb.read()
    blocks= [fromDict(block) for block in blocks]
    return blocks

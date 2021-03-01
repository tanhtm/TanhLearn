# coding:utf-8
import hashlib
from model import Model
from database import ClientDB
import Crypto
import Crypto.Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
import binascii

class Client(Model):
    def __init__ (self, public_key, private_key, identity):
        self.public_key= public_key
        self.private_key= private_key
        self.identity= identity
        
    

def newClient():
    random = Crypto.Random.new().read
    private_key = RSA.generate(1024, random)
    public_key = private_key.publickey()
    identity = binascii.hexlify(public_key.exportKey(format='DER')).decode('ascii')
    cdb = ClientDB()
    cdb.insert({'public_key': public_key.exportKey('PEM').decode("utf-8"),
                'private_key':private_key.exportKey('PEM').decode("utf-8"),
                'identity': identity
               })
    return Client(public_key.exportKey('PEM').decode("utf-8"), 
                  private_key.exportKey('PEM').decode("utf-8"), 
                  identity)

def fromDict(dictClient):
    public_key= dictClient['public_key']
    private_key= dictClient['private_key']
    identity= dictClient['identity']
    return Client(public_key, private_key, identity)

def getClients():
    cdb = ClientDB() 
    clients= cdb.getClients()
    clients= [fromDict(client) for client in clients]
    return clients
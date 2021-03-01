import hashlib
from model import Model
from database import TransactionDB, UnTransactionDB
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
import datetime
import binascii

class Transaction(Model):
    #Client can be both a sender or a recipient of the money.
    #Create a transaction and specify your public address in it.
    
    def __init__(self, sender= None, recipient= None, value= None):
        #Initialization of a transaction class
        self.sender= None
        self.recipient = recipient
        self.value = value
        self.timestamp = str(datetime.datetime.now())
        if not sender is None:
            self.sender = sender.identity
            self.sign_transaction(RSA.importKey(sender.private_key))
        else:
            self.sign= None
        self.hash = self.gen_hash()
        
    def gen_hash(self):
        return hashlib.sha256((str(self.timestamp) + 
                               str(self.sender) + 
                               str(self.value) + 
                               str(self.recipient)+ 
                               str(self.sign)
                              ).encode('utf-8')).hexdigest()  
    
    def sign_transaction(self, sender_private_key):
        #The generated signature is decoded to get the ASCII 
        #representation for printing and storing it in our blockchain.
        private_key = sender_private_key
        signer = PKCS1_v1_5.new(private_key)
        h = SHA.new(str(self.to_dict()).encode('utf8'))
        self.sign= binascii.hexlify(signer.sign(h)).decode('ascii')
        
def fromDict(dictTrans):
    tx= Transaction()
    tx.sender= dictTrans['sender']
    tx.recipient= dictTrans['recipient']
    tx.timestamp= dictTrans['timestamp']
    tx.value= dictTrans['value']
    tx.sign= dictTrans['sign']
    tx.hash= tx.gen_hash()
    return tx
        
def createTransaction(sender, recipientID, value):
    tx= Transaction(sender, recipientID, value)
    tx_dict = tx.to_dict()
    UnTransactionDB().insert(tx_dict)
    return tx

def getUntransactions():
    utxdb= UnTransactionDB()
    utxs= utxdb.read()
    utxs= [ fromDict(utx) for utx in utxs]
    return utxs
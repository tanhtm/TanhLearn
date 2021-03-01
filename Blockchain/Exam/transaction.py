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
    
    def __init__(self, organization= None, recipient= None, recCode= None, date= None, period= None):
        #Initialization of a transaction class
        self.organization= None # Tổ chức cấp
        self.recipient = recipient # Người nhận
        self.timestamp = str(datetime.datetime.now()) 
        if not organization is None:
            self.organization = organization.identity
            self.sign_transaction(RSA.importKey(organization.private_key))
        else:
            self.sign= None
        self.recCode= recCode
        self.date= date  # Ngày cấp
        self.period= period # Thời hạn
        
        self.hash = self.gen_hash()
        
    def gen_hash(self):
        return hashlib.sha256((str(self.timestamp) + 
                               str(self.organization) + 
                               str(self.recipient)+
                               str(self.recCode) + 
                               str(self.date) + 
                               str(self.period) +  
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
    tx.organization= dictTrans['organization']
    tx.recipient= dictTrans['recipient']
    tx.recCode= dictTrans['recCode']
    tx.timestamp= dictTrans['timestamp']
    tx.date= dictTrans['date']
    tx.period= dictTrans['period']
    tx.sign= dictTrans['sign']
    tx.hash= tx.gen_hash()
    return tx
        
def createTransaction(organization, recipientID, recCode, date, period):
    tx= Transaction(organization, recipientID, recCode, date, period)
    tx_dict = tx.to_dict()
    UnTransactionDB().insert(tx_dict)
    return tx

def getUntransactions():
    utxdb= UnTransactionDB()
    utxs= utxdb.read()
    utxs= [ fromDict(utx) for utx in utxs]
    return utxs

def getTransactions():
    txdb= TransactionDB()
    txs= txdb.read()
    txs= [ fromDict(tx) for tx in txs]
    return txs

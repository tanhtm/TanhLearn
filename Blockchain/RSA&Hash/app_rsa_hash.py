import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget,QVBoxLayout, QFormLayout, QPlainTextEdit, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

import hashlib
import os
import Crypto
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP
import base64

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Blockchain'
        self.left = 0
        self.top = 0
        self.width = 600
        self.height = 400
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        self.table_widget = TableWidget(self)
        self.setCentralWidget(self.table_widget)
        self.show()

class TabHash(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        self.textEditInput = QPlainTextEdit(self)
        self.textEditInput.setPlaceholderText('Input')
        self.textEditOutput = QPlainTextEdit(self)
        self.textEditOutput.setPlaceholderText('Output')

        self.pushButtonHash = QPushButton("Hash")
        self.pushButtonHash.clicked.connect(self.on_clickHash)
        self.layout.addWidget(self.textEditInput)
        self.layout.addWidget(self.pushButtonHash)
        self.layout.addWidget(self.textEditOutput)
        self.setLayout(self.layout)

    @pyqtSlot()
    def on_clickHash(self):
        textEditValue = self.textEditInput.document().toPlainText()
        m = hashlib.sha256()
        m.update(textEditValue.encode('utf-8'))
        self.textEditOutput.document().setPlainText(str(m.hexdigest()))

def createKey():
    root = os.getcwd()
    f= open(root + '/key',"w")
    random_generator = Random.new().read
    key = RSA.generate(1024, random_generator)
    f.write(key.exportKey('PEM').decode("utf-8"))

def getKey():
    root = os.getcwd()
    try:
        f= open(root + '/key',"r")
    except:
        createKey()
        f= open(root + '/key',"r")
    return RSA.importKey(f.read())

class TabRSA(QTabWidget):

    def __init__(self, parent):
        super(QTabWidget, self).__init__(parent)
        self.tabKey = TabKey(self)
        self.tabEncode = TabEncode(self)
        self.tabDecode = TabDecode(self)
        self.addTab(self.tabKey, 'Key')
        self.addTab(self.tabEncode, 'Encode' )
        self.addTab(self.tabDecode, 'Decode')


class TabKey(QWidget):

    def setKey(self):
        key = getKey() 
        self.textEditPrivateKey.document().setPlainText(key.exportKey('PEM').decode("utf-8"))
        self.textEditPublicKey.document().setPlainText(key.publickey().exportKey('PEM').decode("utf-8"))
    
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        self.labelPrivateKey = QLabel("Private key")
        self.textEditPrivateKey = QPlainTextEdit(self)
        self.labelPublicKey = QLabel("Public key")
        self.textEditPublicKey = QPlainTextEdit(self)
        self.setKey()
        self.buttonNewKey = QPushButton("New key")
        self.buttonNewKey.clicked.connect(self.on_clickNewKey)

        self.layout.addWidget(self.labelPrivateKey)
        self.layout.addWidget(self.textEditPrivateKey)
        self.layout.addWidget(self.labelPublicKey)
        self.layout.addWidget(self.textEditPublicKey)
        self.layout.addWidget(self.buttonNewKey)
        self.setLayout(self.layout)

    @pyqtSlot()
    def on_clickNewKey(self):
        createKey()
        self.setKey()

class TabEncode(QWidget):

    def setKey(self):
        key = getKey()
        self.textEditPublicKey.document().setPlainText(key.publickey().exportKey('PEM').decode("utf-8"))

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        self.labelPublicKey = QLabel("Public key")
        self.textEditPublicKey = QPlainTextEdit(self)
        self.setKey()
        self.labelInput = QLabel("Input")
        self.textEditInput= QPlainTextEdit(self)
        self.buttonEncode = QPushButton("Encode")
        self.buttonEncode.clicked.connect(self.on_clickEncode)
        self.labelOutput = QLabel("Output")
        self.textEditOutput= QPlainTextEdit(self)


        self.layout.addWidget(self.labelPublicKey)
        self.layout.addWidget(self.textEditPublicKey)
        self.layout.addWidget(self.labelInput)
        self.layout.addWidget(self.textEditInput)
        self.layout.addWidget(self.buttonEncode)
        self.layout.addWidget(self.labelOutput)
        self.layout.addWidget(self.textEditOutput)
        self.setLayout(self.layout)

    @pyqtSlot()
    def on_clickEncode(self):
        textEditValue = self.textEditInput.document().toPlainText()
        key = getKey()
        cipher = PKCS1_OAEP.new(key.publickey())
        ciphertext = cipher.encrypt(str.encode(textEditValue))
        ciphertext = base64.b64encode(ciphertext).decode('utf-8')
        print(ciphertext)
        self.textEditOutput.document().setPlainText(ciphertext)

class TabDecode(QWidget):

    def setKey(self):
        key = getKey()
        self.textEditPrivateKey.document().setPlainText(key.exportKey('PEM').decode("utf-8"))

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        self.labelPrivateKey = QLabel("Private key")
        self.textEditPrivateKey = QPlainTextEdit(self)
        self.setKey()
        self.labelInput = QLabel("Input")
        self.textEditInput= QPlainTextEdit(self)
        self.buttonDecode = QPushButton("Decode")
        self.buttonDecode.clicked.connect(self.on_clickDecode)
        self.labelOutput = QLabel("Output")
        self.textEditOutput= QPlainTextEdit(self)


        self.layout.addWidget(self.labelPrivateKey)
        self.layout.addWidget(self.textEditPrivateKey)
        self.layout.addWidget(self.labelInput)
        self.layout.addWidget(self.textEditInput)
        self.layout.addWidget(self.buttonDecode)
        self.layout.addWidget(self.labelOutput)
        self.layout.addWidget(self.textEditOutput)
        self.setLayout(self.layout)

    @pyqtSlot()
    def on_clickDecode(self):
        textEditValue = self.textEditInput.document().toPlainText()
        key = getKey()
        textEditValue = base64.b64decode(textEditValue.encode('utf-8'))
        cipher = PKCS1_OAEP.new(key)
        ciphertext = cipher.decrypt(textEditValue)
        print(ciphertext)
        ciphertext = ciphertext.decode('utf-8')
        self.textEditOutput.document().setPlainText(str(ciphertext))

class TableWidget(QWidget):
    
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        
        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tabRSA = TabRSA(self)
        self.tabHash = TabHash(self)
        self.tabs.resize(600,400)
        
        # Add tabs
        self.tabs.addTab(self.tabRSA,"RSA")
        self.tabs.addTab(self.tabHash,"Hash - SHA256")  

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

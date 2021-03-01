import MyMath
import MyBase

# Encode
def getPublicKey (file) :
    fi = open(file,"r")
    n = int(fi.readline())
    e = int(fi.readline())
    fi.close()
    return n, e

def getPlaintext (file):
    fi = open(file,"r")
    P = fi.read()
    fi.close()
    return P

def convertStringToInt(P, base):
    R = []
    for i in P:
        c = str(ord(i))
        while len(c) != base:
            c = '0' + c #0000
        R.append(c)
    return R

def createBigInt(R, size_n):
    A = []
    x = ""
    for i in R:
        if len(x) + len(i) >= size_n: # Tối ưu mã hóa nhiều kí tự nhất có thể
            A.append(int(x))
            x = ""
        x+= i
    A.append(int(x))
    return A

def encode(publicKey, P, file= None):
    if not file is None:
        fo = open(file,"w")
    C = ""
    R = convertStringToInt(P, 4)
    n, e= publicKey
    A = createBigInt(R, len(str(n)))
    for i in A:
        M = MyMath.powMod(i,publicKey[1],publicKey[0])
        M = MyBase.toBase(M,64)
        C+= M + ' '
        if not file is None:
            fo.write(M+' ')
    if not file is None:
        fo.close()
    return C

# Decode

def getPrivateKey (file) : # file Privatekey
    fi = open(file,"r")
    n = int(fi.readline())
    d = int(fi.readline())
    fi.close()
    return n, d

def getCiphertext(file): # file Ciphertext
    fi = open(file,"r")
    C = fi.readline()
    fi.close()
    return C

def decode(privateKey, C, fileOut= None, base= 4): # file PlanintextDecode
    C = C.split(" ")
    C = C[:-1]
    if not fileOut is None:
        fo = open(fileOut,"w")
    P = ""
    n, d= privateKey
    for i in C:
        m = MyMath.powMod(MyBase.toInt(i,64),d,n)
        c = str(m)
        while len(c) % base != 0:
            c = '0' + c
        x = 0
        while x != len(c):
            a = c[x:x+base]
            x+= base
            P+= chr(int(a))
            if not fileOut is None:
                fo.write(chr(int(a)))
    if not fileOut is None:
        fo.close()
    return P

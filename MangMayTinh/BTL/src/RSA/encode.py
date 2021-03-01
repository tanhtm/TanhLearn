import MyMath
import MyBase

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

def encode(publicKey, P, file):
	fo = open(file,"w")
	C = ""
	R = convertStringToInt(P, 4)
	n, e= publicKey
	A = createBigInt(R, len(str(n)))
	for i in A:
		M = MyMath.powMod(i,publicKey[1],publicKey[0])
		M = MyBase.toBase(M,64)
		C+= M + ' '
		fo.write(M+' ')
	fo.close()
	return C

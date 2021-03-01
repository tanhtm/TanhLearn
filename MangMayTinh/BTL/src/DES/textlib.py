# Convert Unicode text to binary
def textToBin(text): #16bit
    out= ''
    for letter in text:
        b= format(ord(letter), 'b')
        b= '0'*(16-len(b)) + b
        out += b
    return out

def binToText(btext): #16bit
    out= ''
    for i in range(0,len(btext), 16):
        b= btext[i: i+ 16]
        letter= chr(int(b, 2))
        out+= letter
    return out

def binToHex(bit64):
    return hex(int(bit64, 2))
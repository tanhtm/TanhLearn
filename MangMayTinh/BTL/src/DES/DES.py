from f_function import f
from textlib import *
from key_scheduler import *

# Encode
def genKey():
    k = random.getrandbits(64)
    k = bin(k)[2:].zfill(64)
    return k

def getBlocks(text):
    # Chuyển text về chuỗi nhị phân
    btext= textToBin(text)
    
    #Lấy khối 64bit
    blocks = []
    for i in range(0, len(btext), 64):
        blocks.append(btext[i:i+64])
    return blocks

def encode(text, key= None):
    """
    # text: Văn bản, có thể chứa ký tự đặc biết, có dấu.
    # key: Chuỗi nhị phân, khóa 64bit
    """
    # Tạo khóa con
    keys= key_scheduler(key)
    
    # Tách text thành các khối 64 bit
    blocks = getBlocks(text)

    # Mã hóa từng khối
    e_list = [_cipher(block, keys) for block in blocks]


    # Kết hợp các khối mã hóa thành 1 chuỗi
    out = ''.join(e_list)

    return out

def _cipher(bit64, keys):
    """
    # bit64: Chuỗi nhị phân 64bits
    # keys: 16 round key
    """
    
    # Initial permutation table
    ip = [58, 50, 42, 34, 26, 18, 10, 2,
          60, 52, 44, 36, 28, 20, 12, 4,
          62, 54, 46, 38, 30, 22, 14, 6,
          64, 56, 48, 40, 32, 24, 16, 8,
          57, 49, 41, 33, 25, 17,  9, 1,
          59, 51, 43, 35, 27, 19, 11, 3,
          61, 53, 45, 37, 29, 21, 13, 5,
          63, 55, 47, 39, 31, 23, 15, 7]

    # Final permutation
    fp = [40,  8, 48, 16, 56, 24, 64, 32,
          39,  7, 47, 15, 55, 23, 63, 31,
          38,  6, 46, 14, 54, 22, 62, 30,
          37,  5, 45, 13, 53, 21, 61, 29,
          36,  4, 44, 12, 52, 20, 60, 28,
          35,  3, 43, 11, 51, 19, 59, 27,
          34,  2, 42, 10, 50, 18, 58, 26,
          33,  1, 41,  9, 49, 17, 57, 25]
    

    # Hoán vị các phần tử trong một khối với IP
    bit64= bit64 + '0'*(64 - len(bit64)) # Khối không đủ 64bit
    p = ''.join([ bit64[number-1] for number in ip])

    # Tách p thành 2 phần
    ln = p[:32]
    rn = p[32:]

    # Tiến hành mã hóa 16 vòng
    for i in range(16):
        temp = rn
        rn = bin(int(ln, 2) ^ int(f(rn, keys[i]), 2))[2:].zfill(32) 
        #r_(n+1)= ln XOR f(rn, key)
        ln = temp # ln= rn

    # Kết hợp 2 nửa
    combined = ln + rn
    out = ''.join([combined[number-1] for number in fp])
    
    return out

# Decode

def decode(cipher, key):
    """
    # cipher: Chuỗi nhị phân.
    # key: khóa 64bit
    """
    # Tạo khóa con
    keys= key_scheduler(key)
    
    # Tách cipher thành các khối 64 bit
    blocks = [cipher[i:i+64] for i in range(0, len(cipher), 64)]

    # Giải mã từng khối
    d_list = [_plaintext(block, keys) for block in blocks]

    # Kết hợp lại để tạo chuỗi kết quả
    out = ''.join([binToText(block) for block in d_list])
    
    # Xử lý nếu dữ liệu bị thừa sao khi thêm để đủ 64bit
    if '\x00' in out:
        out= out.replace('\x00', '')
    return out

def _plaintext(bit64, keys):

    # Initial permutation table
    ip = [58, 50, 42, 34, 26, 18, 10, 2,
          60, 52, 44, 36, 28, 20, 12, 4,
          62, 54, 46, 38, 30, 22, 14, 6,
          64, 56, 48, 40, 32, 24, 16, 8,
          57, 49, 41, 33, 25, 17,  9, 1,
          59, 51, 43, 35, 27, 19, 11, 3,
          61, 53, 45, 37, 29, 21, 13, 5,
          63, 55, 47, 39, 31, 23, 15, 7]

    # Final permutation table
    fp = [40,  8, 48, 16, 56, 24, 64, 32,
          39,  7, 47, 15, 55, 23, 63, 31,
          38,  6, 46, 14, 54, 22, 62, 30,
          37,  5, 45, 13, 53, 21, 61, 29,
          36,  4, 44, 12, 52, 20, 60, 28,
          35,  3, 43, 11, 51, 19, 59, 27,
          34,  2, 42, 10, 50, 18, 58, 26,
          33,  1, 41,  9, 49, 17, 57, 25]

    p = ''.join([bit64[number-1] for number in ip])

    # Tách thành 2 nửa
    ln = p[:32]
    rn = p[32:]

    # 16 vòng cho giải mã
    for i in range(15, -1, -1):
        temp = ln
        ln = bin(int(rn, 2) ^ int(f(ln, keys[i]), 2))[2:].zfill(32)
        rn = temp

    # Kết hợp 2 nửa để có kết quả cuối cùng
    combined = ln + rn
    out = ''.join([combined[number-1] for number in fp])
        
    return out
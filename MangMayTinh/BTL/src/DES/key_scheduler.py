#!/usr/bin/env python

import random

"""
DES Key Scheduler:

    - Tạo key 64bit nếu cần.

    - Trả về danh sách 16 key con dạng chuỗi nhị phân

"""

def key_scheduler(key= None):

    # -------------------- Variables -------------------- #
    #
    # k         64-bit key - đầu vào
    # k_prime   Chứa 56-bit hoán vị của key
    # c0        Left half of k_prime
    # d0        Right half of k_prime
    # c_keys    16 28-bit hoán vị của c0 sử dụng lrt
    # d_keys    16 28-bit hoán vị của d0 sử dụng lrt
    # keys      Danh sách 16 keys 48-bit đầu ra
    #
    # --------------------------------------------------- #

    # pc1       Permutation table No. 1 (8 * 7)
    pc1 = [57, 49, 41, 33, 25, 17,  9,
            1, 58, 50, 42, 34, 26, 18,
           10,  2, 59, 51, 43, 35, 27,
           19, 11,  3, 60, 52, 44, 36,
           63, 55, 47, 39, 31, 23, 15,
            7, 62, 54, 46, 38, 30, 22,
           14,  6, 61, 53, 45, 37, 29,
           21, 13,  5, 28, 20, 12,  4]

    # pc2       Permutation table No. 2 (8 * 6)
    pc2 = [14, 17, 11, 24,  1,  5,
           3,  28, 15,  6, 21, 10,
           23, 19, 12,  4, 26,  8,
           16,  7, 27, 20, 13,  2,
           41, 52, 31, 37, 47, 55,
           30, 40, 51, 45, 33, 48,
           44, 49, 39, 56, 34, 53,
           46, 42, 50, 36, 29, 32]
           

    # lrt       Left rotation table
    lrt = [1, 1, 2, 2, 2, 2, 2, 2,
           1, 2, 2, 2, 2, 2, 2, 1]

    # --------------------------------------------------- #
    # Note - Tuy thuận toán bắt đầu với một key 64-bit nhưng DES chỉ lấy 56 bit để tạo khóa
    # bởi vì 8 bit không được sử dụng tạo khóa để kiểm tra khóa vì lỗi đường truyền 
    # có thể làm mất mát các bits.
    
    if key is None:
        k = random.getrandbits(64)
        k = bin(k)[2:].zfill(64)
    else:
        k= key
    

    # Tạo k_prime dùng permutation table 1 - pc1
    k_prime = ""
    for number in pc1:
        k_prime += k[number-1]

    # Chia k_prime thành 2 nửa c0 và d0
    c0 = k_prime[:28]
    d0 = k_prime[28:]

    # Quay c0 và d0 theo lrt - left rotation table
    c_keys = []
    d_keys = []
    for i in range(16):
        num = lrt[i]
   
        temp = c0[0:num]
        c0 = c0[num:] + temp
        c_keys.append(c0)

        temp = d0[0:num]
        d0 = d0[num:] + temp
        d_keys.append(d0)


    # Tạo các khóa con bằng cách kết hợp c_keys[i] và d_keys[i].
    # Dùng pc2 - permutation table 2 để tạo 16 keys 48-bit
    keys = []
    for i in range(16):
        cat = c_keys[i] + d_keys[i]
        temp = ""
        for number in pc2:
            temp += cat[number-1]
        keys.append(temp)

    return keys



import DES

# Triple encryption with 3 separate key sets.
# C = E(D(E(P, k3), k2), k1)
def encode(text, key1, key2, key3):

    return DES.encode(DES.decode(DES.encode(text, key3), key2), key1)


# Triple decryption with 3 separate key sets.
# P = D(E(D(C, k1), k2), k3)
def decode(cipher, key1, key2, key3):

    return DES.decode(DES.encode(DES.decode(cipher, key1), key2), key3)


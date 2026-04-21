import struct
import math

def rotate(x, n):
    x &= 0xFFFFFFFF
    return ((x << n) | (x >> (32 - n))) & 0xFFFFFFFF

def md5_hash(message: bytes):
    A = 0x67452301
    B = 0xEFCDAB89
    C = 0x98BADCFE
    D = 0x10325476

    T = [int(2 ** 32 * abs(math.sin(i + 1))) & 0xFFFFFFFF for i in range(64)]
    s = [7, 12, 17, 22] * 4 + [5, 9, 14, 20] * 4 + [4, 11, 16, 23] * 4 + [6, 10, 15, 21] * 4

    orig_len_bits = (len(message) * 8) & 0xFFFFFFFFFFFFFFFF
    message += b'\x80'
    while (len(message) * 8) % 512 != 448:
        message += b'\x00'

    message += struct.pack('<Q', orig_len_bits)

    for i in range(0, len(message), 64):
        block = message[i:i + 64]
        X = struct.unpack('<16I', block)

        AA, BB, CC, DD = A, B, C, D

        for j in range(64):
            if j < 16 :
                f = (BB & CC) | (~BB & DD)
                g = j
            elif j < 32 :
                f = (BB & DD) | (CC & ~DD)
                g = (5*j+1)%16
            elif j < 48 :
                f = BB^CC^DD
                g = (3*j+5)%16
            else :
                f = CC^(BB | ~DD)
                g = 7*j%16

            f = (f + AA + T[j] + X[g]) & 0xFFFFFFFF
            AA = DD
            DD = CC
            CC = BB
            BB = (BB + rotate(f, s[j])) & 0xFFFFFFFF

        A = (A + AA) & 0xFFFFFFFF
        B = (B + BB) & 0xFFFFFFFF
        C = (C + CC) & 0xFFFFFFFF
        D = (D + DD) & 0xFFFFFFFF

    return struct.pack('<4I', A, B, C, D).hex()

def string_hash(str):
    message = str.encode('utf-8')
    return md5_hash(message)

def file_hash(file):
    try :
        if isinstance(file, str) :
            with open(file, 'rb') as f:
                data = f.read()
        else :
            data = file.read()
        return md5_hash(data)
    except FileNotFoundError:
        return None
    except UnicodeError:
        return None


def verify_file_integrity(file, hash_file):
    try:
        with open(hash_file, 'r') as hf:
            expected_hash = hf.read().strip()

        calculated_hash = file_hash(file)
        if calculated_hash is None:
            return False

        if calculated_hash.lower() == expected_hash.lower():
            return True
        else:
            return False
    except FileNotFoundError:
        return False

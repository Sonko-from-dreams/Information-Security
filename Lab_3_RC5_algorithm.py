import math
import struct
import time
from Lab_1_Randomizer import generate_rand_num
from Lab_2_MD5_algorithm import string_hash

def left_rotate(x, n, w):
    mask = (1 << w) - 1
    n %= w
    return ((x << n) | (x >> (w - n))) & mask

def right_rotate(x, n, w):
    mask = (1 << w) - 1
    n %= w
    x &= mask
    return ((x >> n) | (x << (w - n))) & mask

def key_expansion(w, r, b, key):
    P_Q = {
        16 : [0xb7e1, 0x9e37],
        32 : [0xb7e15163, 0x9e3779b9],
        64 : [0xb7e151628aed2a6b, 0x9e3779b97f4a7c15]
    }
    mask = (1 << w) - 1
    h = string_hash(key)
    if b == 8 :
        K = h[-8:]
    elif b == 32 :
        add_h = string_hash(h)
        K = h + add_h
    else :
        K = (h * (b // 16 + 1))[:b * 2]
    u = w//8
    c = max(1, math.ceil(b / u))
    L = [0]*c
    key_bytes = [int(K[i:i + 2], 16) for i in range(0, len(K), 2)]

    for i in range(b-1, -1, -1) :
        L[i//u] = (L[i//u] << 8) + key_bytes[i]
    t = 2*(r+1)
    S = [0]*t
    S[0] = P_Q[w][0]
    for i in range(1, t) :
        S[i] = (S[i-1] + P_Q[w][1]) & mask

    i, j, A, B = 0, 0, 0 ,0
    for k in range(3*max(t, c)):
        A = S[i] = left_rotate((S[i] + A + B) & mask, 3, w)
        B = L[j] = left_rotate((L[j] + A + B) & mask, (A + B), w)
        i = (i + 1)%t
        j = (j + 1)%c

    return S

def pad(data, block_size):
    padding_len = block_size - (len(data) % block_size)
    padding = bytes([padding_len] * padding_len)
    return data + padding

def unpad(data):
    padding_len = data[-1]
    return data[:-padding_len]

def generate_iv(block_size) -> bytes:

    seed = int(time.time() * 1000000) % 2147483647
    random_numbers = generate_rand_num(10, m=2 ** 31 - 1, a=7**5, c=0, x0=seed)
    raw_data = "".join(map(str, random_numbers))
    hash_hex = string_hash(raw_data)
    iv_full = bytes.fromhex(hash_hex)

    return iv_full[:block_size]


def encrypt(w, r, b, key, text):
        S = key_expansion(w, r, b, key)
        mask = (1 << w) - 1
        fmt = {16: '<H', 32: '<I', 64: '<Q'}[w]
        u = w // 8
        A = struct.unpack(fmt, text[:u])[0]
        B = struct.unpack(fmt, text[u:])[0]

        A = (A + S[0]) & mask
        B = (B + S[1]) & mask
        for i in range(1, r+1):
            A = (left_rotate((A^B), B, w) + S[2*i]) & mask
            B = (left_rotate((B^A), A, w) + S[2*i+1]) & mask
        return struct.pack(fmt, A) + struct.pack(fmt, B)

def decrypt(w, r, b, key, text):
    S = key_expansion(w, r, b, key)
    mask = (1 << w) - 1
    fmt = {16: '<H', 32: '<I', 64: '<Q'}[w]
    u = w // 8
    A = struct.unpack(fmt, text[:u])[0]
    B = struct.unpack(fmt, text[u:])[0]
    for i in range(r, 0, -1):
        B = (right_rotate((B-S[2*i+1]), A, w))^A
        A = (right_rotate((A-S[2*i]), B, w))^B
    B = (B-S[1]) & mask
    A = (A-S[0]) & mask
    return struct.pack(fmt, A) + struct.pack(fmt, B)


def encrypt_cbc(w, r, b, key, text):
    block_size = (2 * w) // 8
    plaintext = pad(text, block_size)

    iv = generate_iv(block_size)

    ciphertext = iv
    prev_block = iv

    for i in range(0, len(plaintext), block_size):
        block = plaintext[i:i + block_size]

        xored_block = bytes([b1 ^ b2 for b1, b2 in zip(block, prev_block)])

        enc_block = encrypt(w, r, b, key, xored_block)

        ciphertext += enc_block
        prev_block = enc_block

    return ciphertext

def file_encrypt(w, r, b, key, file):
    try :
        if isinstance(file, str) :
            with open(file, 'rb') as f:
                data = f.read()
        else :
            data = file.read()
        encrypted_text = encrypt_cbc(w, r, b, key, data)
        return encrypted_text
    except FileNotFoundError:
        return None
    except UnicodeError:
        return None


def decrypt_cbc(w, r, b, key, ciphertext):
    block_size = (2 * w) // 8

    iv = ciphertext[:block_size]
    ciphertext = ciphertext[block_size:]

    plaintext = b""
    prev_block = iv

    for i in range(0, len(ciphertext), block_size):
        block = ciphertext[i:i + block_size]

        dec_block = decrypt(w, r, b, key, block)

        plain_block = bytes([b1 ^ b2 for b1, b2 in zip(dec_block, prev_block)])

        plaintext += plain_block
        prev_block = block

    return unpad(plaintext)

def file_decrypt(w, r, b, key, file):
    try :
        if isinstance(file, str) :
            with open(file, 'rb') as f:
                data = f.read()
        else :
            data = bytes(file.read())
        decrypted_text = decrypt_cbc(w, r, b, key, data)
        return decrypted_text
    except FileNotFoundError:
        return None
    except UnicodeError:
        return None

# w, r, b = 16, 8, 16
# key = "iloveis"
# data = b"I am the hero the world has longed for"
# d = b'HELL'
#
# enc = encrypt(w, r, b, key, d)
# print(f"Зашифровано (hex): {enc.hex()}")
# dec = decrypt(w, r, b, key, enc)
# print(f"Розшифровано: {dec}")
#
# encrypted = encrypt_cbc(w, r, b, key, data)
# print(f"Зашифровано (hex): {encrypted.hex()}")
#
# decrypted = decrypt_cbc(w, r, b, key, encrypted)
# print(f"Розшифровано: {decrypted}")



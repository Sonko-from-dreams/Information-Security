from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key
import time
from Lab_3_RC5_algorithm import file_encrypt

def pr_key_for_download(private_key, passphrase):

    return private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.BestAvailableEncryption(passphrase.encode())
    )


def pb_key_for_download(public_key):

    return public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )


def generate_keys():

    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()

    return private_key, public_key


def encrypt_RCA(message, public_key):

    if isinstance(message, str):
        message = message.encode()

    ciphertext = public_key.encrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return ciphertext


def decrypt_RCA(ciphertext, private_key):

    plaintext = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return plaintext


def encrypt_chunks(data, public_key):

    chunk_size = 190
    encrypted_parts = []

    for i in range(0, len(data), chunk_size):
        chunk = data[i:i + chunk_size]
        encrypted_chunk = public_key.encrypt(
            chunk,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        encrypted_parts.append(encrypted_chunk)

    return b"".join(encrypted_parts)


def decrypt_chunks(encrypted_data, private_key):

    chunk_size = 256
    decrypted_parts = []

    for i in range(0, len(encrypted_data), chunk_size):
        chunk = encrypted_data[i:i + chunk_size]
        decrypted_chunk = private_key.decrypt(
            chunk,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        decrypted_parts.append(decrypted_chunk)

    return b"".join(decrypted_parts)


def save_keys(private_key, public_key, passphrase):

    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.BestAvailableEncryption(passphrase)
    )
    with open('private_key', 'wb') as pem_out:
        pem_out.write(pem)

    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    with open('public_key', 'wb') as pem_out:
        pem_out.write(pem)


def load_private_key_bytes(filename, passphrase):
    try :
        if isinstance(filename, str) :
            with open(filename, 'rb') as f:
                pemlines = f.read()
        else :
            pemlines = filename
        key = load_pem_private_key(pemlines, passphrase.encode())
        return key
    except FileNotFoundError:
        return None
    except UnicodeError:
        return None


def load_public_key_bytes(filename):
    try :
        if isinstance(filename, str) :
            with open(filename, 'rb') as f:
                pemlines = f.read()
        else :
            pemlines = filename
        key = load_pem_public_key(pemlines)
        return key
    except FileNotFoundError:
        return None
    except UnicodeError:
        return None

# filepath = 'D:/Sofi/Information Security/Лабораторна робота №2.pdf'
#
# with open(filepath,'rb') as f:
#     mess = f.read()
# start_time = time.time()
# priv_key, pub_key = generate_keys()
# result = encrypt_chunks(mess, pub_key)
# end_time = time.time()
# print(f"Час виконання бібліотечної RSA :{end_time - start_time} сек")
# w, r, b = 16, 8, 16
# key = "iloveis"
# d = b'HELL'
# start_time = time.time()
# result = file_encrypt(w, r, b, key, filepath)
# end_time = time.time()
# print(f"Час виконання власнонаписаної RC5 : {end_time - start_time} сек")
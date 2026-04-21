from cryptography.hazmat.primitives.asymmetric import dsa
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key
from cryptography.hazmat.primitives.asymmetric import utils

def generate_keys():

    private_key = dsa.generate_private_key(key_size=1024,)
    public_key = private_key.public_key()

    return private_key, public_key

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

def sign_for_download(signature):

    return signature.hex()

def load_signature_from_hex_file(file):

    hex_signature = file.read().decode('utf-8').strip()
    return bytes.fromhex(hex_signature)

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



def sign_message(private_key, message):

    if isinstance(message, str):
        message = message.encode()

    return private_key.sign(
        message,
        hashes.SHA256()
    )

def sign_file(private_key, file):

    file.seek(0)
    chosen_hash = hashes.SHA256()
    hasher = hashes.Hash(hashes.SHA256())

    for chunk in iter(lambda: file.read(4096), b""):
        hasher.update(chunk)

    digest = hasher.finalize()

    return private_key.sign(
        digest,
        utils.Prehashed(chosen_hash)
    )

def verify_message(public_key, message, signature):

    if isinstance(message, str):
        message = message.encode()

    try :
        public_key.verify(
            signature,
            message,
            hashes.SHA256()
        )
        return True

    except Exception as e :
        return False

def verify_file(public_key, file, signature):

    file.seek(0)
    chosen_hash = hashes.SHA256()
    hasher = hashes.Hash(chosen_hash)
    for chunk in iter(lambda: file.read(4096), b""):
        hasher.update(chunk)

    digest = hasher.finalize()

    try:
        public_key.verify(signature, digest, utils.Prehashed(hashes.SHA256()))
        return True

    except Exception:
        return False



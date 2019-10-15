from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.exceptions import InvalidSignature
import codecs
import os

def generate_password():
    randomness = os.urandom(128)
    return codecs.encode(randomness, "base64").decode()

def generate_private_key():
    return rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096,
        backend=default_backend()
    )

def generate_pem(private_key, password):
    return private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.BestAvailableEncryption(password=password)
    )

def generate_public_key(private_key):
    return private_key.public_key()

def generate_public_pem(public_key):
    return public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

def generate_private_pem_string(password_string):
    priv = generate_private_key()
    pem = generate_pem(priv, password_string.encode('utf-8'))
    return pem.decode()

def generate_public_pem_string(private_pem_string, password):
    priv = load_private_key(private_pem_string.encode('utf-8'), password.encode('utf-8'))
    public_key = generate_public_key(priv)
    return generate_public_pem(public_key).decode()

def load_private_key(private_pem, password):
    return serialization.load_pem_private_key(private_pem, backend=default_backend(), password=password)

def load_public_key(public_pem):
    return serialization.load_pem_public_key(public_pem, backend=default_backend())

def verify(public_pem_string, signature, message):
    public_key = load_public_key(public_pem_string.encode('utf-8'))
    signature_binary = codecs.decode(signature.encode('utf-8'), 'base64')
    return verify_binary(public_key, signature_binary, message.encode('utf-8'))

def verify_binary(public_key, signature, message_in_binary):
    try:
        verify_result = public_key.verify(
            signature,
            message_in_binary,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA3_256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA3_256()
        )
    except InvalidSignature:
        return False
    return True

def sign(private_pem_string, password, message):
    priv = load_private_key(private_pem_string.encode('utf-8'), password.encode('utf-8'))
    signature = sign_binary(priv, message.encode('utf-8'))
    return codecs.encode(signature, 'base64').decode()

def sign_binary(private_key, message_in_binary):
    signature = private_key.sign(
        message_in_binary,
        padding.PSS(
                mgf=padding.MGF1(hashes.SHA3_256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
        hashes.SHA3_256()
    )
    return signature






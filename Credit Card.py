Requirement already satisfied: cryptography in c:\users\vinay\anaconda3\lib\site-p
ackages (39.0.1)
Requirement already satisfied: cffi>=1.12 in c:\users\vinay\anaconda3\lib\site-pac
kages (from cryptography) (1.15.1)
Requirement already satisfied: pycparser in c:\users\vinay\anaconda3\lib\site-pack
ages (from cffi>=1.12->cryptography) (2.21)
[notice] A new release of pip is available: 25.3 -> 26.0.1
[notice] To update, run: python.exe -m pip install --upgrade pip
In [1]: !pip install cryptography
In [2]: import os
import base64
import hashlib
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
In [3]: def generate_key():
    master_key = hashlib.sha256(b"super-secure-master-key").digest()
    return master_key
KEY = generate_key()
In [4]: def mask_pan(pan: str) -> str:
    return pan[:4] + " **** **** " + pan[-4:]
In [5]: def encrypt_pan(pan: str, key: bytes) -> str:
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, pan.encode(), None)
    
    encrypted_blob = nonce + ciphertext
    return base64.b64encode(encrypted_blob).decode()
In [6]: def decrypt_pan(encrypted_pan: str, key: bytes) -> str:
    decoded = base64.b64decode(encrypted_pan)
    nonce = decoded[:12]
    ciphertext = decoded[12:]
    
    aesgcm = AESGCM(key)
    pan = aesgcm.decrypt(nonce, ciphertext, None)
    return pan.decode()
In [7]: token_store = {}
def tokenize_pan(pan: str) -> str:
    token = "tok_" + hashlib.sha256(pan.encode()).hexdigest()[:16]
    encrypted_pan = encrypt_pan(pan, KEY)
    
    token_store[token] = encrypted_pan
    return token
In [8]: def detokenize_pan(token: str) -> str:
    encrypted_pan = token_store.get(token)
    if not encrypted_pan:
        raise Exception("Invalid token")
    
    return decrypt_pan(encrypted_pan, KEY)
In [9]: pan = "4111111111111111"
file:///E:/slash mark/card.html 
print("Original PAN (NEVER STORED):", pan)
print("Masked PAN:", mask_pan(pan))
token = tokenize_pan(pan)
print("\nGenerated Token:", token)
retrieved_pan = detokenize_pan(token)
print("Decrypted PAN:", retrieved_pan)
Original PAN (NEVER STORED): 4111111111111111
Masked PAN: 4111 **** **** 1111
Generated Token: tok_9bbef19476623ca5
Decrypted PAN: 4111111111111111
In [ ]:
file:///E:/slash mark/card.html

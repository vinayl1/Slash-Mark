Requirement already satisfied: cryptography in c:\users\vinay\anaconda3\lib\site-p
ackages (39.0.1)
Requirement already satisfied: pillow in c:\users\vinay\anaconda3\lib\site-package
s (9.4.0)
Requirement already satisfied: cffi>=1.12 in c:\users\vinay\anaconda3\lib\site-pac
kages (from cryptography) (1.15.1)
Requirement already satisfied: pycparser in c:\users\vinay\anaconda3\lib\site-pack
ages (from cffi>=1.12->cryptography) (2.21)
Secret Key Generated (keep this safe!)
Image encrypted successfully!
In [1]: !pip install cryptography pillow
In [2]: from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from PIL import Image
import os
import io
In [3]: def generate_key():
    return os.urandom(32)  # 256-bit AES key
key = generate_key()
print("Secret Key Generated (keep this safe!)")
In [4]: def image_to_bytes(image_path):
    img = Image.open(image_path)
    img_format = img.format
    byte_stream = io.BytesIO()
    img.save(byte_stream, format=img_format)
    return byte_stream.getvalue(), img_format
In [5]: def encrypt_image(image_path, key):
    data, img_format = image_to_bytes(image_path)
    iv = os.urandom(16)  # random IV per image
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    
    return encrypted_data, iv, img_format
In [6]: def save_encrypted_file(enc_data, iv, output_file):
    with open(output_file, "wb") as f:
        f.write(iv + enc_data)
In [10]: encrypted_data, iv, img_format = encrypt_image("sample.jpg", key)
save_encrypted_file(encrypted_data, iv, "encrypted_image.bin")
print("Image encrypted successfully!")
In [11]: def decrypt_image(enc_file, key):
    with open(enc_file, "rb") as f:
        iv = f.read(16)
        encrypted_data = f.read()
file:///E:/slash mark/Image encryption.html
cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
decryptor = cipher.decryptor()
padded_data = decryptor.update(encrypted_data) + decryptor.finalize()
unpadder = padding.PKCS7(128).unpadder()
original_data = unpadder.update(padded_data) + unpadder.finalize()
return original_data
In [12]:
In [13]:
In [14]:
Out[14]:
In [15]:
def bytes_to_image(data, output_file, img_format):
img = Image.open(io.BytesIO(data))
img.save(output_file, format=img_format)
decrypted_data = decrypt_image("encrypted_image.bin", key)
bytes_to_image(decrypted_data, "decrypted_image.jpg", img_format)
print("Image decrypted successfully!")
Image decrypted successfully!
Image.open("sample.jpg")
Image.open("decrypted_image.jpg")
file:///E:/slash mark/Image encryption.html
Out[15]:
file:///E:/slash mark/Image encryption.html

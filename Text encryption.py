
[1]: from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.backends import default_backend
import os
[2]: def derive_key(password: str, salt: bytes)-> bytes:
kdf = PBKDF2HMAC(
algorithm=hashes.SHA256(),
length=32,
# AES-256
salt=salt,
iterations=100000,
backend=default_backend()
)
return kdf.derive(password.encode())
[3]: def encrypt_text(plaintext: str, password: str)-> bytes:
salt = os.urandom(16) # Random salt
iv = os.urandom(16)
# Random IV
key = derive_key(password, salt)
padder = padding.PKCS7(128).padder()
padded_data = padder.update(plaintext.encode()) + padder.finalize()
cipher = Cipher(
algorithms.AES(key),
modes.CBC(iv),
backend=default_backend()
)
encryptor = cipher.encryptor()
ciphertext = encryptor.update(padded_data) + encryptor.finalize()
# Store: salt + iv + ciphertext
return salt + iv + ciphertext
[4]: def decrypt_text(encrypted_data: bytes, password: str)-> str:
salt = encrypted_data[:16]
iv = encrypted_data[16:32]
ciphertext = encrypted_data[32:]
key = derive_key(password, salt)
cipher = Cipher(
algorithms.AES(key),
modes.CBC(iv),
backend=default_backend()
)
decryptor = cipher.decryptor()
padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
unpadder = padding.PKCS7(128).unpadder()
plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
return plaintext.decode()
[5]: text = "CONFIDENTIAL DATA"
password = "my_secure_password"
cipher1 = encrypt_text(text, password)
cipher2 = encrypt_text(text, password)
print("Ciphertext 1:", cipher1.hex())
print("Ciphertext 2:", cipher2.hex())
print("Different outputs?", cipher1 != cipher2)
Ciphertext 1: 8853d73e0e87ad9c320adf6ca79d082e3877da382535df5baf15bc0b5bdf8badd1
3c30d6436782251502c71a3e00ad2fbe3a46c4fb420cb2ba58fe32c5fb2206
Ciphertext 2: 2f3e94f548329bba73ebb3cfe151a78e7f66917b7fc4c4e51b96346765888cdd66
6c62e2ff8644ce06fdeda587f3a8fb8523c112720369b1482d264cd9519374
Different outputs? True
[6]: print("Decrypted Text:", decrypt_text(cipher1, password))
Decrypted Text: CONFIDENTIAL DATA
[7]: pip install ipywidgets
Requirement already satisfied: ipywidgets in c:\users\akhil\anaconda3\lib\site
packages (8.0.4)
Requirement already satisfied: ipykernel>=4.5.1 in
c:\users\vinay\anaconda3\lib\site-packages (from ipywidgets) (6.25.0)
Requirement already satisfied: ipython>=6.1.0 in
c:\users\vinay\anaconda3\lib\site-packages (from ipywidgets) (8.12.2)
Requirement already satisfied: traitlets>=4.3.1 in
c:\users\akhil\anaconda3\lib\site-packages (from ipywidgets) (5.7.1)
Requirement already satisfied: widgetsnbextension~=4.0 in
c:\users\akhil\anaconda3\lib\site-packages (from ipywidgets) (4.0.5)
Requirement already satisfied: jupyterlab-widgets~=3.0 in
c:\users\akhil\anaconda3\lib\site-packages (from ipywidgets) (3.0.5)
Requirement already satisfied: comm>=0.1.1 in c:\users\akhil\anaconda3\lib\site
packages (from ipykernel>=4.5.1->ipywidgets) (0.1.2)
Requirement already satisfied: debugpy>=1.6.5 in
c:\users\vinay\anaconda3\lib\site-packages (from ipykernel>=4.5.1->ipywidgets)
(1.6.7)
Requirement already satisfied: jupyter-client>=6.1.12 in
c:\users\vinay\anaconda3\lib\site-packages (from ipykernel>=4.5.1->ipywidgets)
(7.4.9)
Requirement already satisfied: jupyter-core!=5.0.*,>=4.12 in
c:\users\vinay\anaconda3\lib\site-packages (from ipykernel>=4.5.1->ipywidgets)
(5.3.0)
Requirement already satisfied: matplotlib-inline>=0.1 in
c:\users\vinay\anaconda3\lib\site-packages (from ipykernel>=4.5.1->ipywidgets)
(0.1.6)
Requirement already satisfied: nest-asyncio in
c:\users\vinay\anaconda3\lib\site-packages (from ipykernel>=4.5.1->ipywidgets)
(1.5.6)
Requirement already satisfied: packaging in c:\users\vinay\anaconda3\lib\site
packages (from ipykernel>=4.5.1->ipywidgets) (23.0)
Requirement already satisfied: psutil in c:\users\vinay\anaconda3\lib\site
packages (from ipykernel>=4.5.1->ipywidgets) (5.9.0)
Requirement already satisfied: pyzmq>=20 in c:\users\vinay\anaconda3\lib\site
packages (from ipykernel>=4.5.1->ipywidgets) (23.2.0)
Requirement already satisfied: tornado>=6.1 in
c:\users\vinay\anaconda3\lib\site-packages (from ipykernel>=4.5.1->ipywidgets)
(6.3.2)
Requirement already satisfied: backcall in c:\users\vinay\anaconda3\lib\site
packages (from ipython>=6.1.0->ipywidgets) (0.2.0)
Requirement already satisfied: decorator in c:\users\vinay\anaconda3\lib\site
packages (from ipython>=6.1.0->ipywidgets) (5.1.1)
Requirement already satisfied: jedi>=0.16 in c:\users\vinay\anaconda3\lib\site
packages (from ipython>=6.1.0->ipywidgets) (0.18.1)
Requirement already satisfied: pickleshare in c:\users\vinay\anaconda3\lib\site
packages (from ipython>=6.1.0->ipywidgets) (0.7.5)
Requirement already satisfied: prompt-toolkit!=3.0.37,<3.1.0,>=3.0.30 in
c:\users\vinay\anaconda3\lib\site-packages (from ipython>=6.1.0->ipywidgets)
(3.0.36)
Requirement already satisfied: pygments>=2.4.0 in
c:\users\vinay\anaconda3\lib\site-packages (from ipython>=6.1.0->ipywidgets)
(2.15.1)
Requirement already satisfied: stack-data in c:\users\vinay\anaconda3\lib\site
packages (from ipython>=6.1.0->ipywidgets) (0.2.0)
Requirement already satisfied: colorama in c:\users\vinay\anaconda3\lib\site
packages (from ipython>=6.1.0->ipywidgets) (0.4.6)
Requirement already satisfied: parso<0.9.0,>=0.8.0 in
c:\users\vinay\anaconda3\lib\site-packages (from
jedi>=0.16->ipython>=6.1.0->ipywidgets) (0.8.3)
Requirement already satisfied: entrypoints in c:\users\vinay\anaconda3\lib\site
packages (from jupyter-client>=6.1.12->ipykernel>=4.5.1->ipywidgets) (0.4)
Requirement already satisfied: python-dateutil>=2.8.2 in
c:\users\vinay\anaconda3\lib\site-packages (from jupyter
client>=6.1.12->ipykernel>=4.5.1->ipywidgets) (2.8.2)
Requirement already satisfied: platformdirs>=2.5 in
c:\users\vinay\anaconda3\lib\site-packages (from jupyter
core!=5.0.*,>=4.12->ipykernel>=4.5.1->ipywidgets) (3.10.0)
Requirement already satisfied: pywin32>=300 in
c:\users\vinay\anaconda3\lib\site-packages (from jupyter
core!=5.0.*,>=4.12->ipykernel>=4.5.1->ipywidgets) (305.1)
Requirement already satisfied: wcwidth in c:\users\vinay\anaconda3\lib\site
packages (from prompt
toolkit!=3.0.37,<3.1.0,>=3.0.30->ipython>=6.1.0->ipywidgets) (0.2.5)
Requirement already satisfied: executing in c:\users\vinay\anaconda3\lib\site
packages (from stack-data->ipython>=6.1.0->ipywidgets) (0.8.3)
Requirement already satisfied: asttokens in c:\users\vinay\anaconda3\lib\site
packages (from stack-data->ipython>=6.1.0->ipywidgets) (2.0.5)
Requirement already satisfied: pure-eval in c:\users\vinay\anaconda3\lib\site
packages (from stack-data->ipython>=6.1.0->ipywidgets) (0.2.2)
Requirement already satisfied: six>=1.5 in c:\users\vinay\anaconda3\lib\site
packages (from python-dateutil>=2.8.2->jupyter
client>=6.1.12->ipykernel>=4.5.1->ipywidgets) (1.16.0)
Note: you may need to restart the kernel to use updated packages.
[8]: import ipywidgets as widgets
from IPython.display import display
[9]: input_text = widgets.Textarea(
description="Plain Text",
placeholder="Enter text here",
layout=widgets.Layout(width="100%", height="80px")
)
password_input = widgets.Password(
description="Password",
placeholder="Enter password"
)
output_text = widgets.Textarea(
description="Output",
layout=widgets.Layout(width="100%", height="80px")
)
encrypt_btn = widgets.Button(description="Encrypt", button_style="success")
decrypt_btn = widgets.Button(description="Decrypt", button_style="info")
[10]: from IPython.display import display, Markdown
display(Markdown("## ￿ Text Encryption App (AES-256 + Salt + IV)"))
0.1 ￿ Text Encryption App (AES-256 + Salt + IV)
[11]: plain_input = widgets.Textarea(
placeholder="Enter plain text OR encrypted hex here",
layout=widgets.Layout(width="100%", height="80px")
)
password_input = widgets.Password(
placeholder="Enter password",
layout=widgets.Layout(width="50%")
)
output_box = widgets.Textarea(
placeholder="Output will appear here",
layout=widgets.Layout(width="100%", height="80px")
)
encrypt_btn = widgets.Button(
description="Encrypt",
button_style="success"
)
decrypt_btn = widgets.Button(
description="Decrypt",
button_style="info"
)
[12]: def encrypt_action(b):
encrypted = encrypt_text(plain_input.value, password_input.value)
output_box.value = encrypted.hex()
def decrypt_action(b):
encrypted_bytes = bytes.fromhex(plain_input.value)
output_box.value = decrypt_text(encrypted_bytes, password_input.value)
encrypt_btn.on_click(encrypt_action)
decrypt_btn.on_click(decrypt_action)
[13]: display(
widgets.VBox([
plain_input,
password_input,
widgets.HBox([encrypt_btn, decrypt_btn]),
output_box
])
)
VBox(children=(Textarea(value='', layout=Layout(height='80px', width='100%'),␣
↪placeholder='Enter plain text OR…
[14]: pip install nbconvert
Requirement already satisfied: nbconvert in c:\users\akhil\anaconda3\lib\site
packages (6.5.4)
Requirement already satisfied: lxml in c:\users\akhil\anaconda3\lib\site
packages (from nbconvert) (4.9.2)
Requirement already satisfied: beautifulsoup4 in
c:\users\vinay\anaconda3\lib\site-packages (from nbconvert) (4.12.2)
Requirement already satisfied: bleach in c:\users\vinay\anaconda3\lib\site
packages (from nbconvert) (4.1.0)
Requirement already satisfied: defusedxml in c:\users\vinay\anaconda3\lib\site
packages (from nbconvert) (0.7.1)
Requirement already satisfied: entrypoints>=0.2.2 in
c:\users\vinay\anaconda3\lib\site-packages (from nbconvert) (0.4)
Requirement already satisfied: jinja2>=3.0 in c:\users\vinay\anaconda3\lib\site
packages (from nbconvert) (3.1.2)
Requirement already satisfied: jupyter-core>=4.7 in
c:\users\vinay\anaconda3\lib\site-packages (from nbconvert) (5.3.0)
Requirement already satisfied: jupyterlab-pygments in
c:\users\vinay\anaconda3\lib\site-packages (from nbconvert) (0.1.2)
Requirement already satisfied: MarkupSafe>=2.0 in
c:\users\vinay\anaconda3\lib\site-packages (from nbconvert) (2.1.1)
Requirement already satisfied: mistune<2,>=0.8.1 in
c:\users\vinay\anaconda3\lib\site-packages (from nbconvert) (0.8.4)
Requirement already satisfied: nbclient>=0.5.0 in
c:\users\vinay\anaconda3\lib\site-packages (from nbconvert) (0.5.13)
Requirement already satisfied: nbformat>=5.1 in
c:\users\vinay\anaconda3\lib\site-packages (from nbconvert) (5.7.0)
Requirement already satisfied: packaging in c:\users\vinay\anaconda3\lib\site
packages (from nbconvert) (23.0)
Requirement already satisfied: pandocfilters>=1.4.1 in
c:\users\vinay\anaconda3\lib\site-packages (from nbconvert) (1.5.0)
Requirement already satisfied: pygments>=2.4.1 in
c:\users\vinay\anaconda3\lib\site-packages (from nbconvert) (2.15.1)
Requirement already satisfied: tinycss2 in c:\users\vinay\anaconda3\lib\site
packages (from nbconvert) (1.2.1)
Requirement already satisfied: traitlets>=5.0 in
c:\users\vinay\anaconda3\lib\site-packages (from nbconvert) (5.7.1)
Requirement already satisfied: platformdirs>=2.5 in
c:\users\vinay\anaconda3\lib\site-packages (from jupyter-core>=4.7->nbconvert)
(3.10.0)
Requirement already satisfied: pywin32>=300 in
c:\users\vinay\anaconda3\lib\site-packages (from jupyter-core>=4.7->nbconvert)
(305.1)
Requirement already satisfied: jupyter-client>=6.1.5 in
c:\users\vinay\anaconda3\lib\site-packages (from nbclient>=0.5.0->nbconvert)
(7.4.9)
Requirement already satisfied: nest-asyncio in
c:\users\vinay\anaconda3\lib\site-packages (from nbclient>=0.5.0->nbconvert)
(1.5.6)
Requirement already satisfied: fastjsonschema in
c:\users\vinay\anaconda3\lib\site-packages (from nbformat>=5.1->nbconvert)
(2.16.2)
Requirement already satisfied: jsonschema>=2.6 in
c:\users\vinay\anaconda3\lib\site-packages (from nbformat>=5.1->nbconvert)
(4.17.3)
Requirement already satisfied: soupsieve>1.2 in
c:\users\vinay\anaconda3\lib\site-packages (from beautifulsoup4->nbconvert)
(2.4)
Requirement already satisfied: six>=1.9.0 in c:\users\akhil\anaconda3\lib\site
packages (from bleach->nbconvert) (1.16.0)
Requirement already satisfied: webencodings in
c:\users\vinay\anaconda3\lib\site-packages (from bleach->nbconvert) (0.5.1)
Requirement already satisfied: attrs>=17.4.0 in
c:\users\vinay\anaconda3\lib\site-packages (from
jsonschema>=2.6->nbformat>=5.1->nbconvert) (22.1.0)
Requirement already satisfied: pyrsistent!=0.17.0,!=0.17.1,!=0.17.2,>=0.14.0 in
c:\users\vinay\anaconda3\lib\site-packages (from
jsonschema>=2.6->nbformat>=5.1->nbconvert) (0.18.0)
Requirement already satisfied: python-dateutil>=2.8.2 in
c:\users\vinay\anaconda3\lib\site-packages (from jupyter
client>=6.1.5->nbclient>=0.5.0->nbconvert) (2.8.2)
Requirement already satisfied: pyzmq>=23.0 in c:\users\vinay\anaconda3\lib\site
packages (from jupyter-client>=6.1.5->nbclient>=0.5.0->nbconvert) (23.2.0)
Requirement already satisfied: tornado>=6.2 in
c:\users\vinay\anaconda3\lib\site-packages (from jupyter
client>=6.1.5->nbclient>=0.5.0->nbconvert) (6.3.2)
Note: you may need to restart the kernel to use updated packages.
[15]: display(
widgets.VBox([
plain_input,
password_input,
widgets.HBox([encrypt_btn, decrypt_btn]),
output_box
])
)
VBox(children=(Textarea(value='HELLO', layout=Layout(height='80px',␣
↪width='100%'), placeholder='Enter plain te…
[ ]:

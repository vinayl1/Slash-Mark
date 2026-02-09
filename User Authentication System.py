Requirement already satisfied: bcrypt in c:\users\vinay\anaconda3\lib\site-package
s (3.2.0)
Requirement already satisfied: pyjwt in c:\users\vinay\anaconda3\lib\site-packages 
(2.4.0)
Collecting pyotp
  Downloading pyotp-2.9.0-py3-none-any.whl.metadata (9.8 kB)
Requirement already satisfied: cffi>=1.1 in c:\users\vinay\anaconda3\lib\site-pack
ages (from bcrypt) (1.15.1)
Requirement already satisfied: six>=1.4.1 in c:\users\vinay\anaconda3\lib\site-pac
kages (from bcrypt) (1.16.0)
Requirement already satisfied: pycparser in c:\users\vinay\anaconda3\lib\site-pack
ages (from cffi>=1.1->bcrypt) (2.21)
Downloading pyotp-2.9.0-py3-none-any.whl (13 kB)
Installing collected packages: pyotp
Successfully installed pyotp-2.9.0
[notice] A new release of pip is available: 25.3 -> 26.0.1
[notice] To update, run: python.exe -m pip install --upgrade pip
In [1]: !pip install bcrypt pyjwt pyotp
In [2]: import bcrypt
import jwt
import time
import pyotp
import hashlib
In [3]: JWT_SECRET = "super-secret-key"
JWT_ALGO = "HS256"
JWT_EXP = 3600  # 1 hour
In [4]: users_db = {}
password_reset_tokens = {}
In [5]: def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
def verify_password(password: str, hashed: bytes) -> bool:
    return bcrypt.checkpw(password.encode(), hashed)
In [6]: def signup(username, password, role="user", mfa_enabled=False):
    if username in users_db:
        raise Exception("User already exists")
    users_db[username] = {
        "password": hash_password(password),
        "role": role,
        "mfa": mfa_enabled,
        "mfa_secret": pyotp.random_base32() if mfa_enabled else None
    }
    return "Signup successful"
In [7]: def login(username, password, otp=None):
    user = users_db.get(username)
    if not user:
        raise Exception("User not found")
    if not verify_password(password, user["password"]):
        raise Exception("Invalid credentials")
    if user["mfa"]:
file:///E:/slash mark/user.html
        totp = pyotp.TOTP(user["mfa_secret"])
        if not otp or not totp.verify(otp):
            raise Exception("Invalid MFA code")
    payload = {
        "sub": username,
        "role": user["role"],
        "exp": int(time.time()) + JWT_EXP
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGO)
    return token
In [8]: def verify_jwt(token):
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO])
    except jwt.ExpiredSignatureError:
        raise Exception("Session expired")
    except:
        raise Exception("Invalid token")
In [9]: def authorize(token, required_role):
    payload = verify_jwt(token)
    if payload["role"] != required_role:
        raise Exception("Access denied")
    return True
In [10]: def request_password_reset(username):
    token = hashlib.sha256((username + str(time.time())).encode()).hexdigest()
    password_reset_tokens[token] = username
    return token
In [11]: def reset_password(reset_token, new_password):
    username = password_reset_tokens.get(reset_token)
    if not username:
        raise Exception("Invalid reset token")
    users_db[username]["password"] = hash_password(new_password)
    del password_reset_tokens[reset_token]
    return "Password reset successful"
In [12]: def get_mfa_qr(username):
    user = users_db[username]
    totp = pyotp.TOTP(user["mfa_secret"])
    return totp.provisioning_uri(username, issuer_name="SecureApp")
In [13]: # Signup users
signup("admin", "Admin@123", role="admin", mfa_enabled=True)
signup("user1", "User@123")
# MFA code generation (simulating authenticator app)
otp = pyotp.TOTP(users_db["admin"]["mfa_secret"]).now()
# Login
admin_token = login("admin", "Admin@123", otp=otp)
user_token = login("user1", "User@123")
print("Admin JWT:", admin_token)
print("User JWT:", user_token)
# RBAC test
authorize(admin_token, "admin")  # OK
# authorize(user_token, "admin") # 
❌
 would fail
file:///E:/slash mark/user.html
# Password reset
reset_token = request_password_reset("user1")
reset_password(reset_token, "NewPassword@123")
Out[13]:
In [ ]:
Admin JWT: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhZG1pbiIsInJvbGUiOiJhZG
1pbiIsImV4cCI6MTc3MDQ0NjkyNX0.2SRs6c_jFLSfC8gt9JrrxSbUysZYUTgXm795H5yneOo
User JWT: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1c2VyMSIsInJvbGUiOiJ1c2V
yIiwiZXhwIjoxNzcwNDQ2OTI2fQ.-FTtuTa1nhKY71gCcWoyo06A9HuSVqBqCOOpRg_9AZ4
'Password reset successful'
file:///E:/slash mark/user.html

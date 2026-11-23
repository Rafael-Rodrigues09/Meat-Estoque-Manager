from pwdlib import PasswordHash

pwd_hash = PasswordHash.recommended()

def generate_hash(password):
    return pwd_hash.hash(password)

def verify_hash(password, password_hash):
    return pwd_hash.verify(password, password_hash)

import bcrypt

# Hash function using brcypt
# Function returns the password_hash
def hash_pw(password: str) -> bytes:
    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(bytes(password, 'utf8'), salt)

    return password_hash

def check_pw(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(bytes(password, 'utf8'), hashed_password)

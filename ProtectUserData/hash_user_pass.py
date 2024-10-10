import hashlib

def get_password_hash(user_pass):
    password_bytes = user_pass.encode('utf-8')
    hash_algorithm = hashlib.sha256()
    hash_algorithm.update(password_bytes)
    hashed_password = hash_algorithm.hexdigest()
    return hashed_password

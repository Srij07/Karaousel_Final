def verify_password(password: str, hashed_password: str):
    return (password == hashed_password)
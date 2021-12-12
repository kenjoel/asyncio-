from passlib.context import CryptContext

crypto_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password):
    return crypto_ctx.hash(password)


def verify_password(password, hashed):
    return crypto_ctx.verify(password, hashed)

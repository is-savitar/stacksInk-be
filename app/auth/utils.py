from passlib.context import CryptContext

passwd_context = CryptContext(
    schemes=["bcrypt"],
)


def generate_passwd_hash(password: str) -> str:
    password_hash = passwd_context.hash(password)
    return password_hash


def verify_passwd_hash(password: str, hashed_password: str) -> bool:
    password_hash = passwd_context.verify(password, hashed_password)
    return password_hash

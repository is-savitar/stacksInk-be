from sqlmodel import SQLModel, Field, Relationship

from app.core.models import UUIDModel, TimestampModel


class ValidateField(SQLModel):
    field: str
    value: str

class StxAddress(SQLModel):
    stx_address_mainnet: str | None = Field(default=None, unique=True)


class UserBase(StxAddress):
    username: str | None = Field(default=None, min_length=3, unique=True)
    name: str | None = Field(None, min_length=3)
    profile_picture: str | None= Field(None, min_length=3, max_length=100)
    about_me: str | None= Field(None, min_length=3, max_length=100)
#     Stacks stuff
    prevTxID: str | None = Field(default=None)
    stx_address_testnet: str | None = Field(default=None, unique=True)
    btc_address_mainnet: str | None = Field(default=None, unique=True)
    btc_address_testnet: str | None = Field(default=None, unique=True)

class UserProfile(UserBase):
    followers_count: int = Field(default=0)

class User(UserBase, UUIDModel, TimestampModel, table=True):
    __tablename__ = "users"
    password_hash: str = Field(exclude=True)
    blogs :  list["Blog"] = Relationship(back_populates="user", cascade_delete=True)

class UserCreate(StxAddress):
    password: str = Field()


class UserRead(UserBase, UUIDModel):
    pass

class UserUpdate(UserBase):
    pass

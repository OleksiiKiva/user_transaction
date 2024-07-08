from datetime import date

from pydantic import BaseModel, ConfigDict

from db.transaction_type import TransactionType


class TransactionBase(BaseModel):
    transaction_type: TransactionType
    amount: int


class TransactionCreate(TransactionBase):
    user_id: int


class Transaction(TransactionBase):
    pass

    model_config = ConfigDict(from_attributes=True)


# ---------------------
class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    pass


class UserCreateResponse(BaseModel):
    id: int


class User(UserBase):
    id: int
    transactions: list[Transaction]

    model_config = ConfigDict(from_attributes=True)

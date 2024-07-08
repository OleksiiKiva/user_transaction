from sqlalchemy.orm import Session
from sqlalchemy.sql import functions

from db import models
import schemas


# --add user---------------------------------------
def get_user_by_username(db: Session, username: str):
    return (
        db.query(models.DBUser)
        .filter(models.DBUser.username == username)
        .first()
    )


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.DBUser(
        username=user.username,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


# --get user---------------------------------------
def get_user(db: Session, user_id: int):
    return db.query(models.DBUser).filter(models.DBUser.id == user_id).first()


# --get all users----------------------------------
def get_users_list(db: Session):
    return db.query(models.DBUser).all()


# --add transaction--------------------------------
def get_user_id(db: Session, user_id: int):
    return db.query(models.DBUser).filter(models.DBUser.id == user_id).first()


def create_transaction(db: Session, transaction: schemas.TransactionCreate):
    db_transaction = models.DBTransaction(
        transaction_type=transaction.transaction_type,
        amount=transaction.amount,
        user_id=transaction.user_id,
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)

    return db_transaction


# --statistics-------------------------------------
def total_transactions(db: Session):
    return db.query(models.DBTransaction.id).count()


def total_amount(db: Session):
    return db.query(functions.sum(models.DBTransaction.amount)).scalar()

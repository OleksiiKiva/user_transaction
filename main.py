from fastapi import FastAPI, Depends, HTTPException, Request
from jinja2 import FileSystemLoader, Environment
from sqlalchemy.orm import Session, sessionmaker
from starlette.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

import crud
import schemas
from db.engine import SessionLocal, engine
from db.models import admin, DBTransaction

app = FastAPI(title="User-Transaction")
templates = Jinja2Templates(directory="templates")

# Mount admin to your app
admin.mount_to(app)


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# @app.get("/test/")
def total_transactions():
    count = crud.total_transactions(db=SessionLocal())
    amaont = crud.total_amount(db=SessionLocal())
    return {"count": count, "amount": amaont}


@app.post("/users/", response_model=schemas.UserCreateResponse)
def add_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db=db, username=user.username)

    if db_user:
        raise HTTPException(
            status_code=400, detail="Such username already exists"
        )

    return crud.create_user(db=db, user=user)


@app.get("/users/{user_id}/", response_model=schemas.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db=db, user_id=user_id)

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    return db_user


@app.get("/users/", response_model=list[schemas.User])
def get_all_users(db: Session = Depends(get_db)):
    return crud.get_users_list(db=db)


@app.post("/transactions/", response_model=schemas.Transaction)
def add_transaction(
    transaction: schemas.TransactionCreate, db: Session = Depends(get_db)
):
    db_transaction = crud.get_user_id(db=db, user_id=transaction.user_id)

    if not db_transaction:
        raise HTTPException(
            status_code=400, detail="There is no user with this ID"
        )

    return crud.create_transaction(db=db, transaction=transaction)

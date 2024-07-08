from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from starlette_admin import CustomView
from starlette_admin.contrib.sqla import Admin, ModelView

from db.engine import Base, engine
from db.transaction_type import TransactionType


class DBUser(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(256), nullable=False, unique=True)

    transactions = relationship("DBTransaction", back_populates="user")


class DBTransaction(Base):
    __tablename__ = "transaction"

    id = Column(Integer, primary_key=True, index=True)
    transaction_type = Column(Enum(TransactionType), nullable=False)
    amount = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"))

    user = relationship(DBUser)


# Create an empty admin interface
admin = Admin(engine, title="User-Transaction")

admin.add_view(
    CustomView(
        label="Statistic", template_path="statistic.html", add_to_menu=False
    )
)
admin.add_view(ModelView(DBUser))
admin.add_view(ModelView(DBTransaction))

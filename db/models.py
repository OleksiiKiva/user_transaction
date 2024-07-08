from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from starlette.requests import Request
from starlette.responses import Response
from starlette.templating import Jinja2Templates
from starlette_admin import CustomView
from starlette_admin.contrib.sqla import Admin, ModelView

import crud
from db.engine import Base, engine, SessionLocal
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


class StatisticAdminView(CustomView):
    def total_transactions(self):
        count = crud.total_transactions(db=SessionLocal())
        amount = crud.total_amount(db=SessionLocal())
        return {"count": count, "amount": amount}

    async def render(
        self, request: Request, templates: Jinja2Templates
    ) -> Response:
        """Default methods to render view. Override this methods to add your custom logic."""
        context = self.total_transactions()
        context.update({"request": request, "title": self.title(request)})

        return templates.TemplateResponse(self.template_path, context)


# Create an empty admin interface
admin = Admin(engine, title="User-Transaction")

admin.add_view(
    StatisticAdminView(
        label="Statistic",
        template_path="statistic.html",
        add_to_menu=False,
    )
)
admin.add_view(ModelView(DBUser))
admin.add_view(ModelView(DBTransaction))

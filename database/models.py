from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class TestCustomer(Base):
    __tablename__ = "test_customers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(nullable=False)

    stripe_account: Mapped["StripeConnectAccount"] = relationship(back_populates="")


class StripeConnectAccount(Base):
    __tablename__ = "teacher_connect_account"

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("test_customers.id"))
    account_id: Mapped[str] = mapped_column(nullable=True)
    account_email: Mapped[str] = mapped_column(nullable=True)
    account_status: Mapped[bool] = mapped_column(nullable=False)

    test_customer: Mapped["TestCustomer"] = relationship(back_populates="stripe_account")


class TeacherPaymentIntent(Base):
    __tablename__ = "teacher_payment_intents"

    id: Mapped[int] = mapped_column(primary_key=True)
    intent_id: Mapped[str] = mapped_column(nullable=False)
    amount: Mapped[int] = mapped_column(nullable=False)
    intent_status: Mapped[str] = mapped_column(nullable=False)

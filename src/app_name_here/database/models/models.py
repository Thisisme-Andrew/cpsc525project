"""
Database model definitions.
"""

from sqlalchemy import *
from datetime import datetime, timezone
from sqlalchemy.orm import declarative_base, mapped_column, Mapped
from sqlalchemy.orm import relationship
from decimal import Decimal

Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    email: Mapped[str] = mapped_column(String(100), primary_key=True)
    password: Mapped[str] = mapped_column(String(100))

    account: Mapped["Account"] = relationship(
        "Account", back_populates="user", uselist=False, cascade="all, delete-orphan"
    )
    budgets: Mapped["Budget"] = relationship(
        "Budget", back_populates="user", cascade="all, delete-orphan"
    )


class Account(Base):
    __tablename__ = "account"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_email: Mapped[str] = mapped_column(ForeignKey("user.email"))
    # max balance with this is $99,999,999.99
    balance: Mapped[Decimal] = mapped_column(Numeric(10, 2))

    user: Mapped[User] = relationship("User", back_populates="account")
    transactions: Mapped[list["Transaction"]] = relationship(
        "Transaction", back_populates="account", cascade="all, delete-orphan"
    )


class Transaction(Base):
    __tablename__ = "transaction"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    account_id: Mapped[int] = mapped_column(ForeignKey("account.id"))
    date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now(timezone.utc)
    )
    starting_balance: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    ending_balance: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    # Max of $99,999,999.99
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    transaction_type: Mapped[str] = mapped_column(String(10))
    description: Mapped[str] = mapped_column(String(200), nullable=True)

    account: Mapped[Account] = relationship("Account", back_populates="transactions")


class Budget(Base):
    __tablename__ = "budget"

    user_email: Mapped[str] = mapped_column(ForeignKey("user.email"), primary_key=True)
    name: Mapped[str] = mapped_column(String(100), primary_key=True)
    # Max of $99,999,999.99 for goal and balance
    goal: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    balance: Mapped[Decimal] = mapped_column(Numeric(10, 2))

    user: Mapped[User] = relationship("User", back_populates="budgets")

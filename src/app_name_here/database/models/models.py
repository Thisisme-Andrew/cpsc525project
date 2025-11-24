"""
Database model definitions.
"""

from sqlalchemy import *
from sqlalchemy.orm import declarative_base, mapped_column, Mapped

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    email: Mapped[str] = mapped_column(String(100), primary_key=True)
    password: Mapped[str] = mapped_column(String(100))

class FooBar(Base):
    __tablename__ = 'foobar'

    foo: Mapped[int] = mapped_column(Integer, primary_key=True)
    bar: Mapped[String] = mapped_column(String(100))

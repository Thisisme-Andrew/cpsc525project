"""Application package initialization."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Define the local database.
engine = create_engine("sqlite:///database.db")

# Create the SQLAlchemy session.
db = sessionmaker(bind=engine)()

# Make the application runner available after the database is defined. DO NOT REMOVE.
from .runner import run

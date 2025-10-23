"""
Application package initialization.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Define the local database.
engine = create_engine('sqlite:///../database/app_name_here.db')

# Create the SQLAlchemy session.
db = sessionmaker(bind=engine)()

# Make the application runner available after the database is defined
from .runner import run

# database.py
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timezone

# Load environment variables from .env file
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Define the Images model
class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    public_url = Column(String)
    current_time_utc = datetime.now(timezone.utc)
    upload_time = Column(DateTime, default=current_time_utc)

# Define the Transformations model
class Transformation(Base):
    __tablename__ = "transformations"

    id = Column(Integer, primary_key=True, index=True)
    image_id = Column(Integer, ForeignKey("images.id"))
    transformation_type = Column(String)
    parameters = Column(String)  # Store parameters as a string, e.g., JSON format
    current_time_utc = datetime.now(timezone.utc)
    timestamp = Column(DateTime, default=current_time_utc)

# Create the tables
Base.metadata.create_all(bind=engine)
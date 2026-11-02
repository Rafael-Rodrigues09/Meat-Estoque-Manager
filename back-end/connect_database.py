from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
from sqlalchemy import create_engine
import os

load_dotenv()
url = os.getenv('DATA_URL')
engine = create_engine(url)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
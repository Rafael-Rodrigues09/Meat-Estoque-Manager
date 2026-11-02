from connect_database import Base
from sqlalchemy import Column, Integer, String, Float, DateTime, Date, Boolean
from datetime import datetime, timezone

class Meats(Base):
    __tablename__ = 'meats'
    id = Column(Integer, primary_key=True)
    name = Column(String(40))
    usage_kg = Column(Float)
    rest_kg = Column(Float)

class History(Base):
    __tablename__ = 'history'
    id = Column(Integer, primary_key=True)
    name = Column(String(40))
    type = Column(String)
    value = Column(Float)
    is_reversed = Column(Boolean, default=False)
    date = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class Lot(Base):
    __tablename__ = 'lot'
    id = Column(Integer, primary_key=True)
    name = Column(String(40))
    initial_kg = Column(Float)
    current_kg = Column(Float)
    expiration_date = Column(Date)
    entry_date = Column(DateTime(timezone=True), default= lambda: datetime.now(timezone.utc))
    is_active = Column(Boolean, default=True)
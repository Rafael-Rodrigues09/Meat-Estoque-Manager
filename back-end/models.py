from connect_database import Base
from sqlalchemy import Column, Integer, String, Numeric, DateTime, Date, Boolean
from datetime import datetime, timezone

class Meats(Base):
    __tablename__ = 'meats'
    id = Column(Integer, primary_key=True)
    name = Column(String(40))
    usage_kg = Column(Numeric(10, 3))
    rest_kg = Column(Numeric(10, 3))

class History(Base):
    __tablename__ = 'history'
    id = Column(Integer, primary_key=True)
    name = Column(String(40))
    type = Column(String)
    value = Column(Numeric(10, 3))
    is_reversed = Column(Boolean, default=False)
    date = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class Lot(Base):
    __tablename__ = 'lot'
    id = Column(Integer, primary_key=True)
    name = Column(String(40))
    initial_kg = Column(Numeric(10, 3))
    current_kg = Column(Numeric(10, 3))
    expiration_date = Column(Date)
    entry_date = Column(DateTime(timezone=True), default= lambda: datetime.now(timezone.utc))
    is_active = Column(Boolean, default=True)
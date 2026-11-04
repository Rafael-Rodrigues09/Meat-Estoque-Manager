from pydantic import BaseModel, Field
from datetime import date
from decimal import Decimal

class ModeloRegistro(BaseModel):
    name: str
    value: Decimal = Field(gt=0)

class ModeloLot(BaseModel):
    name: str
    value: Decimal = Field(gt=0)
    expiration_date: date
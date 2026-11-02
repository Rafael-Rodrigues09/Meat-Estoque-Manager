from pydantic import BaseModel, Field
from datetime import date

class ModeloRegistro(BaseModel):
    name: str
    value: float = Field(gt=0)

class ModeloLot(BaseModel):
    name: str
    value: float = Field(gt=0)
    expiration_date: date
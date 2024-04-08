from pydantic import BaseModel
from typing import Tuple, Optional

class Address(BaseModel):
    address_id: int
    street: str
    city: str
    state: str
    country: str
    latitude: float
    longitude: float

class AddressCreate(BaseModel):
    street: str
    city: str
    state: str
    country: str
    latitude: float
    longitude: float

class AddressUpdate(BaseModel):
    address_id: int
    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class AddressDelete(BaseModel):
    address_id: int


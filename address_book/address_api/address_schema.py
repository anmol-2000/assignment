from pydantic import BaseModel
from typing import Union, Optional

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

    class Config:
        json_schema_extra = {
            "example": {
                "street": "Ragupathy Apartment",
                "city": "Bangalore",
                "state": "Karnataka",
                "country": "India",
                "latitude": 12.938482,
                "longitude": 77.74771
            }
        }

class AddressUpdate(BaseModel):
    address_id: int
    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    class Config:
        json_schema_extra = {
            "example": {
                "address_id": 1,
                "street": "Ragupathy Apartment 6th Cross Street",
                "city": "Bangalore"
            }
        }

class AddressDelete(BaseModel):
    address_id: int
    class Config:
        json_schema_extra = {
            "example": {
                "address_id": 2,
            }
        }

class AddressFetch(BaseModel):
    latitude: float
    longitude: float
    distance: Union[int, float]
    class Config:
        json_schema_extra = {
            "example": {
                "latitude": 12.9213,
                "longitude": 77.747711,
                "distance": 50
            }
        }



from fastapi import APIRouter
from fastapi.responses import JSONResponse
from typing import List

# Importing the Pydantic schemas and the AddressModel class
from address_api.address_schema import Address, AddressCreate, AddressDelete, AddressUpdate, AddressFetch
from address_api.address_model import AddressModel

# Creating an APIRouter instance
router = APIRouter(prefix="/address")

# Creating an instance of the AddressModel class
address_model = AddressModel()

# Endpoint for creating a new address
@router.post("")
async def create_address(address: AddressCreate) -> dict:
    """
    Endpoint to create a new address.
    """
    # Calling the add_address method of the AddressModel class
    response = await address_model.add_address(address)
    # Handling error responses
    if isinstance(response, dict) and "error" in list(response.keys()):
        return JSONResponse(status_code=400, content=response)
    # Returning success response
    return JSONResponse(response)


@router.put("")
async def update_address(address: AddressUpdate) -> dict:
    """
    Endpoint to update an existing address.
    """
    # Fetching the existing address from the database
    db_address = await address_model.get_address(address.address_id)

    if db_address is None:
        return JSONResponse(status_code=404, content='Address not found for the given id')
    # Calling the update address method of the AddressModel class
    response = await address_model.update_address(address)
    # Handling error responses
    if isinstance(response, dict) and "error" in list(response.keys()):
        return JSONResponse(status_code=400, content=response)
    return JSONResponse(response)


@router.delete("/{address_id}")
async def delete_address(address: AddressDelete) -> dict:
    """
    Endpoint to delete an address by its ID.
    """
    # Fetching the existing address from the database
    db_address = await address_model.get_address(address.address_id)
    if db_address is None:
        return JSONResponse(status_code=404, content='Address not found for the given id')
    # Calling the delete address method of the AddressModel class
    response = await address_model.delete_address(address.address_id)
    # Handling error responses
    if isinstance(response, dict) and "error" in list(response.keys()):
        return JSONResponse(status_code=400, content=response)
    return JSONResponse(response)

# Endpoint for retrieving addresses within a given distance and location coordinates
@router.post("/by_distance")
async def get_address_by_distnace(address: AddressFetch) -> List[Address]:
    """
    Endpoint to retrieve addresses within a given distance and location coordinates.
    """
    # Calling the get_address_by_distance method of the AddressModel class
    response = await address_model.get_address_by_distance(address)
    # Handling error responses
    if isinstance(response, dict) and "error" in list(response.keys()):
        return JSONResponse(status_code=400, content=response)
    return response

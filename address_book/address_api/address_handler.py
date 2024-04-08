from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from typing import List, Optional
from address_api.address_schema import Address, AddressCreate, AddressDelete, AddressUpdate
from address_api.address_model import AddressModel

router = APIRouter()

@router.post("/address")
async def create_address(address: AddressCreate):
    address_model = AddressModel()
    response = await address_model.add_address(address)
    if isinstance(response, dict) and "error" in list(response.keys()):
        return JSONResponse(status_code=400, content=response)    
    return JSONResponse(response)

@router.put("/address")
async def update_address(address: AddressUpdate):
    if address.address_id is None:
        return JSONResponse(status_code=400, content='address_id is empty')

    address_model = AddressModel()

    db_address = await address_model.get_address(address.address_id)
    if db_address is None:
        return JSONResponse(status_code=404, content='Address not found for the given id')

    response = await address_model.update_address(address)
    if isinstance(response, dict) and "error" in list(response.keys()):
        return JSONResponse(status_code=400, content=response)    
    return JSONResponse(response)

@router.delete("/address/{address_id}")
async def delete_address(address: AddressDelete):
    if address.address_id is None:
        return JSONResponse(status_code=400, content='address_id is empty')

    address_model = AddressModel()

    db_address = await address_model.get_address(address.address_id)
    if db_address is None:
        return JSONResponse(status_code=404, content='Address not found for the given id')
    
    response = address_model.delete_address(address.address_id)
    if isinstance(response, dict) and "error" in list(response.keys()):
        return JSONResponse(status_code=400, content=response)    
    return JSONResponse(response)







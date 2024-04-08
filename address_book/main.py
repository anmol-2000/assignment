import uvicorn
from fastapi import FastAPI
from address_api.address_handler import router

app = FastAPI()
app.include_router(router)

if __name__ == '__main__':
    uvicorn.run(app, host="localhost", port=9020)
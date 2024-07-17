import logging
from fastapi import FastAPI
from dotenv import load_dotenv

from api.main import api_router

load_dotenv()

app = FastAPI()
logging.basicConfig(level=logging.INFO)
app.include_router(api_router)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)
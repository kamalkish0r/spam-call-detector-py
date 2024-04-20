import json
import logging
from fastapi import FastAPI
from starlette.requests import Request
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import HTMLResponse

from api.main import api_router
from dotenv import load_dotenv
load_dotenv()
import os

app = FastAPI()
logging.basicConfig(level=logging.INFO)
app.include_router(api_router)
app.add_middleware(SessionMiddleware, secret_key=os.getenv('SECRET_KEY'))


@app.get('/')
async def homepage(request: Request):
    user = request.session.get('user')
    if user:
        data = json.dumps(user)
        html = (
            f'<pre>{data}</pre>'
            '<a href="/logout">logout</a>'
        )
        return HTMLResponse(html)
    return HTMLResponse('<a href="/login">login</a>')


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)
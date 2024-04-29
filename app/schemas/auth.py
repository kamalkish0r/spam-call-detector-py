from pydantic import BaseModel

class LoginRequest(BaseModel):
    authToken: str

class TokenResponse(BaseModel):
    token: str
    token_type: str = "Bearer"
from pydantic import BaseModel

class UserDetails(BaseModel):
  name: str
  email: str
  picture: str

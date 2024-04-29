from pydantic import BaseModel

class SpamStatus(BaseModel):
    spam: bool

class MarkSpamResponse(BaseModel):
    status: str
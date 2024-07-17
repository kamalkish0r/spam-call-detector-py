from pydantic import BaseModel
from pydantic import BaseModel, validator
import phonenumbers


class SpamStatus(BaseModel):
    spam: bool

class MarkSpamResponse(BaseModel):
    status: str


class PhoneNumber(BaseModel):
    number: str

    @validator('number')
    def validate_phone_number(cls, v):
        try:
            parsed_number = phonenumbers.parse(v, None)
            if not phonenumbers.is_valid_number(parsed_number):
                raise ValueError("Invalid phone number")
        except phonenumbers.phonenumberutil.NumberParseException:
            raise ValueError("Invalid phone number")
        return v
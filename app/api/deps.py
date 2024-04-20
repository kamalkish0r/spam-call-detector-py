from fastapi.security import OAuth2PasswordBearer, Oauth2


# need to read about security in fastapi
# need read about either pydantic or sqlmodel
# If I understand how security works in fastapi application then only I can figure out how can I use google auth for authentication and jwt tokens for authorization
# If I undestand about sqlmodel or pydantic then it would be easy for me to handle data & interact with db
reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"token"
)
from passlib.context import CryptContext

#Secret key for encoding jwt-token
SECRET_KEY = "secret_key"

#Algorithm for encoding
ALGORITHM = "HS256"

#time life for access token
ACCESS_TOKEN_EXPIRE_MINUTES = 3

#time line for refresh token
REFRESH_TOKEN_EXPIRE_MINUTES = 5

#Method for encrypting password
PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")

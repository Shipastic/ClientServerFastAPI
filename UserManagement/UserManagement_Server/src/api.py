from jsonrpcserver import method, Result, Success
from fastapi import FastAPI, Depends, HTTPException
from jwt import InvalidTokenError
from core.dto.MappingDTO import * 
from core.dto.UserDTO import UserDTO
from domain.UsersBase import UserCreate
from domain_service.JWTTokenService import JWTTokenService
from domain_service.UserService import UserService
from domain.Constants import *
from domain_service.PasswordService import *
from core.RepositoryImplement.UserRepoImplement import UserRepoImplementation

app = FastAPI()

jwtToken = JWTTokenService()

#Method for get all users
@method
@app.get("/users", response_model=None)
def get_all_users(token:str) -> Result:   
    try:
        mapping_users_dto = MappingDTO()
        user_dto = jwtToken.verify_token(token)
        if user_dto.role == "admin" or user_dto.role == "user":
            users = mapping_users_dto.get_users_dto_from_db()
            return Success(users) 
        else:
            raise HTTPException(status_code=403, detail="Access Denied")    

    except PermissionError:
        raise InvalidTokenError(status_code=401, detail="Invalid token")

#Method for create users
@method
@app.post("/create_user", response_model=None) 
def create_user(user: UserCreate, user_dto: UserDTO = Depends(jwtToken.verify_token))-> Result:
    try:
        pwd_service = PasswordService()
        user_repository = UserRepoImplementation()
        user_service = UserService()
        create_user =  user_service.set_user_create_fields(user,pwd_service,user_repository, user_dto)
        if create_user.isCreated:
            return Success({"message": "User created successfully", "new user": {user.username}})
        else:
            raise HTTPException(status_code=400, detail="Error on user create")

    except PermissionError:
        raise HTTPException(status_code=401, detail="Access Denied")   


#Method for login
@method
@app.post("/login", response_model=None)
def login(username: str, password: str) -> Result:    
    try:
        user_service = UserService()
        token_pair = user_service.get_user_tokens(username, password)
        return Success(token_pair)
    except Exception:
        raise HTTPException(status_code=401, detail="You are not authorization")



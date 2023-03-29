from jsonrpcserver import method, Result, Success
from fastapi import FastAPI, Depends, HTTPException
from jwt import InvalidTokenError
from core.dto.MappingDTO import MappingDTO 
from core.dto.UserDTO import UserDTO
from domain.UsersBase import UserCreate
from domain_service.JWTTokenService import JWTTokenService
from domain_service.UserService import UserService
from domain.Constants import *
from domain_service.PasswordService import *
from core.RepositoryImplement.UserRepoImplement import UserRepoImplementation
from core.RepositoryImplement.TokenRepoImplement import TokenRepoImplementation

app = FastAPI()


jwtToken = JWTTokenService()
user_repo = UserRepoImplementation()
token_repo = TokenRepoImplementation()

#Method for get all users
@method
@app.get("/users", response_model=None)
def get_all_users(token:str) -> Result:   
    try:
        user_dto = jwtToken.verify_token(token)
        if user_dto.role == "admin" or user_dto.role == "user":
            users = user_repo.get_users()      
            usersDict = list(users)
            return Success(usersDict) 
        else:
            raise HTTPException(status_code=403, detail="Access Denied")    

    except PermissionError:
        raise InvalidTokenError(status_code=401, detail="Invalid token")

#Method for create users
@method
@app.post("/create_user", response_model=None) 
def create_user(user: UserCreate, user_dto: UserDTO = Depends(jwtToken.verify_token))-> Result:
    try:
        if user_dto is None:
            return {"error": "Invalid token"}
        if user_dto.role != "admin":
            return {"error": "Access denied"}

        pwd_service = PasswordService()
        hashed_password = pwd_service.generate_hash(user.password)

        is_user_created = user_repo.create_user(user.username, user.role, hashed_password)

        if is_user_created:
            return Success({"message": "User created successfully", "new user": {user.username}})
        else:
            raise HTTPException(status_code=400, detail="Error on user create")

    except PermissionError:
        raise HTTPException(status_code=401, detail="Access Denied")   


#Method for login
@method
@app.post("/login", response_model=None)
def login(username: str, password: str) -> Result:
    mapping = MappingDTO()
    pwd_service = PasswordService()

    auth_user = user_repo.get_user(username)
    user_dto =  mapping.set_user_dto_fields(auth_user)

    hashed_password = pwd_service.generate_hash(password)

    if UserService.is_user_verification(hashed_password, auth_user[2]):    
        TokenPair = jwtToken.generation_pair_tokens(user_dto)
        JWTTokenService.save_refresh_token(user_dto,TokenPair[1])
        return  Success({"access_token": TokenPair[0],  "refresh_token": TokenPair[1]})
    else:
       raise HTTPException(status_code=401, detail="You are not authorization")



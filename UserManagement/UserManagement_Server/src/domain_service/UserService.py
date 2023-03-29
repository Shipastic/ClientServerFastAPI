from domain_service.PasswordService import *
from domain_service.JWTTokenService import *
from core.dto.MappingDTO import * 
from core.dto.UserDTO import *
from domain.Token import Token
from domain.Constants import *
from core.RepositoryImplement.UserRepoImplement import UserRepoImplementation


class UserService:
    def __init__(self):
        self._token_expiration_minutes = ACCESS_TOKEN_EXPIRE_MINUTES
        self._token_expiration_minutes_refresh = REFRESH_TOKEN_EXPIRE_MINUTES
        self.isCreated: str
        self.password_hash: str
        self.is_valid_role: bool

    #Method for Compare passwords
    def is_user_password_verification(self, password:str, password_from_db:str):  
        pwd_service = PasswordService()
        password_hash = pwd_service.generate_hash(password)             
        return True if password_hash == password_from_db else False

    #Method for get tokens in user_dto
    def get_user_tokens(self, username:str, password:str):
        mapping = MappingDTO()
        jwt_token = JWTTokenService()
        user_dto =  mapping.set_user_dto_fields_from_db(username)     
        if self.is_user_password_verification(password, user_dto.password):    
            self.set_user_pair_tokens(user_dto)
            jwt_token.save_refresh_token(user_dto)
            return  {"access_token": user_dto.token_access,  "refresh_token": user_dto.token_refresh}
        else:
            return None

    #Method for create two tokens
    def set_user_pair_tokens(self,user_dto: UserDTO) -> UserDTO:
        jwt_token = JWTTokenService()
        token_access = Token("access", self._token_expiration_minutes)
        token_refresh = Token("refresh", self._token_expiration_minutes_refresh)
        user_dto.token_access = jwt_token.create_jwt_token(user_dto,token_access)
        user_dto.token_refresh = jwt_token.create_jwt_token(user_dto,token_refresh)
    
    #Method for check role user
    def check_user_role(self, user_dto: UserDTO):
        if user_dto is None:
            return {"error": "Invalid token"}
        if user_dto.role != "admin":
            return {"error": "Access denied"}

    def set_user_create_fields(self,user: UserCreate, user_dto: UserDTO):
        try:
            pwd_service = PasswordService()
            user_repository = UserRepoImplementation()
            self.is_valid_role = self.check_user_role(user_dto)
            self.password_hash = pwd_service.generate_hash(user.password)
            self.isCreated = user_repository.create_user(user.username, user.role, self.password_hash)
            return self
        except:
            return None
   

    
import jwt
from datetime import datetime
from core.dto.UserDTO import UserDTO
from domain.UsersBase import *
from domain.Constants import *
from domain.Token import Token
from core.RepositoryImplement.TokenRepoImplement import  TokenRepoImplementation
from core.dto.MappingDTO import * 

tokenRepo = TokenRepoImplementation()


class JWTTokenService:

    def __init__(self):
        self._secret_key = SECRET_KEY
        self._algorithm = ALGORITHM

    # Method for verification tokens
    def verify_token(self, verifiable_token: str) -> UserDTO:
        try:
            user_mapping = MappingDTO()
            token_properties = self.decode_token(verifiable_token)
            user_dto = user_mapping.set_user_dto_fields_from_token(token_properties)
            if self.check_lifetime_token(user_dto.expiration_token):
                if user_dto.username is None or user_dto.role is None or user_dto.expiration_token is None:
                    return None           
            return user_dto
        except jwt.DecodeError:
            return None
       
    # Method for generation new JWT-token 
    def create_jwt_token(self, user_dto: UserDTO, token: Token) -> str:
        payload= (
                {
                    "sub": user_dto.username,
                    "exp": token.token_lifetime,
                    "iss": "backend-api",
                    "usr": user_dto.id,
                    "type": token.type,
                    "role": user_dto.role
                }
            )
        create_token = jwt.encode(payload, self._secret_key, algorithm=self._algorithm)      
        return create_token

    #МMethod for create and update refresh token
    def save_refresh_token(self,user_dto:UserDTO):                  
        try:
            if tokenRepo.get_refresh_token(user_dto.id):
                tokenRepo.update_refresh_token(user_dto)
            else :   
                tokenRepo.insert_refresh_token(user_dto)  
        except Exception:
            return Exception.__name__

    #Method for check token lifetime
    def check_lifetime_token(self,access_token_expires_at: int) -> bool:
        try:
            ts = int(f'{access_token_expires_at}')
            token_lifetime = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%dT%H:%M:%SZ')
            utc_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
            if utc_time <= token_lifetime:
                return True
            else:
                return False
        except:
            return None

    #Method for decode token
    def decode_token(self, verifiable_token: str):
        decoded_token = jwt.decode(jwt=verifiable_token, key= self._secret_key, algorithms=self._algorithm)
        return decoded_token

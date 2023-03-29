from .UserDTO import *
from .TokenDTO import TokenDTO
from core.RepositoryImplement.UserRepoImplement import UserRepoImplementation

user_repo = UserRepoImplementation()

class MappingDTO:
    
    #Method for setting user fields from data
    def set_user_dto_fields_from_db(self,username: str) -> UserDTO:
        try:
            auth_user = user_repo.get_user(username)
            user_dto = UserDTO()
            user_dto.id = auth_user[0]
            user_dto.username = auth_user[1]
            user_dto.password = auth_user[2]
            user_dto.role = auth_user[3]
            return user_dto
        except :
            return None

    #Method for get user list from data base
    def get_users_dto_from_db(self):
        try:
            auth_users = user_repo.get_users()
            users_dto = list()          
            for user in auth_users:
                user_dto = UserDTO()
                user_dto.id = user[0]
                user_dto.username = user[1]
                user_dto.password = user[2]
                user_dto.role = user[3]
                users_dto.append(user_dto)
            return users_dto
        except :
            return None

    #Method for setting token fields from data
    def set_refresh_token_dto_field(self, token_implement : tuple) -> TokenDTO:
        try:
            token_dto = TokenDTO()
            token_dto.user_id  = token_implement[0]
            token_dto.token = token_implement[1]
            token_dto.created_at = token_implement[2]
            token_dto.updated_at = token_implement[3]
            token_dto.expires_at = token_implement[4]
            return token_dto
        except:
            return None

    #Method for setting fields user_dto from token
    def set_user_dto_fields_from_token(self, token_payload_dict:dict):
        user_dto= UserDTO()
        user_dto.username = token_payload_dict.get("sub")
        user_dto.role = token_payload_dict.get("role")
        user_dto.expiration_token = token_payload_dict.get("exp")
        return user_dto
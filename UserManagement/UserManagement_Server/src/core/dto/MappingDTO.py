from .UserDTO import *
from .TokenDTO import TokenDTO

class MappingDTO:
    
    #Method for setting user fields from data
    def set_user_dto_fields(self,user_implement: tuple) -> UserDTO:
        try:
            user_dto = UserDTO()
            user_dto.id = user_implement[0]
            user_dto.username = user_implement[1]
            user_dto.password = user_implement[2]
            user_dto.role = user_implement[3]
            return user_dto
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
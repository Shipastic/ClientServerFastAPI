from ..db.PostgresDbConnection import *
from ..dto.UserDTO import UserDTO
from ..Repository.TokenRepository import TokenRepository
from domain.Constants import REFRESH_TOKEN_EXPIRE_MINUTES, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import datetime, timedelta

class TokenRepoImplementation(TokenRepository):
    
    id : int
    user_id : str
    token : str
    expires_at : datetime
    created_at:  datetime
    updated_at:  datetime
    time_death_token_refresh = datetime.utcnow() +timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    time_death_token_access = datetime.utcnow() +timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    dbConn = DbConnection(
                            "UserManagement",
                            "postgres",
                            "postgres",
                            "127.0.0.1",
                            "5432"
                            )

    #Method for insert refresh token in table refresh_tokens                        
    def insert_refresh_token(self, user_dto:UserDTO):
        query = f"INSERT INTO refresh_tokens (user_id, token, expires_at) VALUES ('{user_dto.id}', '{user_dto.token_refresh}', '{self.time_death_token_refresh}')"
        try:
            self.dbConn.connect()
            self.dbConn.execute_query(query)  
            self.dbConn.disconnect()
            return True
        except Exception as e:
            self.dbConn.disconnect() 
            print(f"Failed to insert refresh_token: {e}")
            return False

    #Method for update refresh_token        
    def update_refresh_token(self, user_dto:UserDTO):
        query = f"UPDATE refresh_tokens SET token = '{user_dto.token_refresh}', expires_at = '{self.time_death_token_refresh}'  WHERE user_id ='{user_dto.id}'"
        try:
            self.dbConn.connect()
            self.dbConn.execute_query(query)  
            self.dbConn.disconnect()
            return True       
        except Exception as e:
            self.dbConn.disconnect() 
            print(f"Failed to update refresh_token: {e}")
            return False 

    #Method for get info from refresh token
    def get_refresh_token(self, id):
        query = f"SELECT user_id, token, created_at, updated_at, expires_at FROM refresh_tokens WHERE user_id='{id}'"
        try:
            self.dbConn.connect()
            token_base = self.dbConn.execute_query_select_one(query)
            self.dbConn.disconnect()  
            return token_base      
        except Exception as e:
            self.dbConn.disconnect()          
            print(f"Failed to get user from token: {e}")
            return None


   
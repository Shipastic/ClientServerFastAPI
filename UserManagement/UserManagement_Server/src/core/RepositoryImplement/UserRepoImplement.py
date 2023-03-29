from ..db.PostgresDbConnection import *
from ..Repository.UserRepository import UserRepository
class UserRepoImplementation(UserRepository):
    
    id : int
    username : str
    password : str
    role : str

    dbConn = DbConnection(
                            "UserManagement",
                            "postgres",
                            "postgres",
                            "127.0.0.1",
                            "5432"
                            )

    #MEthod for get one user 
    def get_user(self, username):
        query = f"SELECT * FROM users Where username='{username}'"
        try:
            self.dbConn.connect()
            auth_user = self.dbConn.execute_query_select_one(query)
            self.dbConn.disconnect()
            return auth_user      
        except Exception as e:
            self.dbConn.disconnect() 
            print(f"Failed to get user: {e}")
            return None



    #Method for get all users in table users
    def get_users(self):
        query = f"SELECT id, username, password, role FROM users"
        try:
            self.dbConn.connect()
            users = self.dbConn.execute_query_select_all(query)
            self.dbConn.disconnect()
            return users
        except Exception as e:
            self.dbConn.disconnect() 
            print(f"Failed to get users: {e}")
            return None


    
    #Method for create user
    def create_user(self, username, role, password):
        try:
            query = f"INSERT INTO users (username, password, role) VALUES ('{username}', '{password}', '{role}')"
            self.dbConn.connect()
            self.dbConn.execute_query(query)  
            self.dbConn.disconnect()
            return True         
        except Exception as e:
            self.dbConn.disconnect() 
            print(f"Failed to create user: {e}")
            return False

            

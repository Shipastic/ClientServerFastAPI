class UserService:
    
    #Method for Compare passwords
    @staticmethod
    def is_user_verification(password:str, password_from_db:str):               
        return True if password == password_from_db else False

    
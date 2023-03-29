import bcrypt 

class PasswordService:
    #Method for generation hash
    def generate_hash(self,password:str):
        mySalt = b'$2b$12$vXEOL6iZB47d5I0uw.THQu'
        bytePwd = password.encode('utf-8')
        hash = bcrypt.hashpw(bytePwd, mySalt)
        return hash.decode()



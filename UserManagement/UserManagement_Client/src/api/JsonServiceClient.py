from ..client.ClientSetting import ClientSetting
import requests
from json import dumps, loads
class JsonServiceClient:
    
    currentMethod = "/login"
    @staticmethod
    def get_string_query(): 
        clientStr = ClientSetting(protocol="http", host="localhost", port="8000/")          
        stringResult = f"{clientStr.protocol}://{clientStr.host}:{clientStr.port}"
        return stringResult

    @staticmethod
    def login(urlString:str, login:str, password:str):
        method = "login" 
        headers = {"content-type": "application/json"}     
        response =  requests.post(f"{urlString}{method}?username={login}&password={password}", headers=headers) 
        print(response)
        response_dict = response.json()
        parsed = response_dict['_value']      
        inParsed = parsed[0]
        get_token = inParsed['access_token']
        if response.reason  == 'OK':
            return True, get_token
        else:
            return False

            
    @staticmethod
    def get_users(urlString:str,token:str):
        method = "users"
        response =  requests.get(f"{urlString}{method}?token={token}")
        return response.json()

    @staticmethod
    def create_user(urlString:str, login, role, token, password):
        method = "create_user"
        headers = {'Content-Type: application/json'}
        data = {'username': 'admin','role': 'admin','password': 'admin'}
        response = requests.post(f"{urlString}{method}?token={token}", data={'username': 'admin','role': 'admin','password': 'admin'})
        print(response)
        response_dict = response.json()


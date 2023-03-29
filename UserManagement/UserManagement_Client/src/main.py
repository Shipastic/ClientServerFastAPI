from .api.JsonServiceClient import JsonServiceClient
from .api.PermissionCheckService import *

credential = False
print("Welcome to API")

def auth():
    global credential
    global token
    global login
    global password
    while not credential:   
        login = input("Enter your login: ")
        password = input("Enter your password: ")
        method = "login"
        url = JsonServiceClient.get_string_query()
        is_result, token = JsonServiceClient.login(url, login, password)
        if is_result:
            credential = True
            print(f"Congratulation, {login}, you are authenticated!")
        else:
            print('Invalid password, please try again.')
        

auth()

if credential:
    print('You are now authenticated!')
else:
    print('Authentication failed.')

role = check_permission_token(token)
get_current_role = role['role']
url = JsonServiceClient.get_string_query()
if get_current_role == 'admin':
    print("The following methods are available to you:")
    print("1: Create User")
    print("2: View Users")
    print("3: Exit")
    user_choice = int(input("Enter number: \n"))
    match user_choice:
        case 1:
            print(JsonServiceClient.create_user(url, login, get_current_role, token, password))
            
        case 2:
            print(JsonServiceClient.get_users(url,token))
            
        case 3:
            print("Exit to the program")
            exit
   
else:
    print("The following methods are available to you:")
    print("1: View Users")
    input("Enter number 1 for run view users list:")
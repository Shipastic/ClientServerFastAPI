# ClientServerFastAPI
### Проект реализует работу сервиса авторизации и аутентификации с использованием JWT-токена.
- Данный проект демонстрирует работу по протоколу Json-RPC.
- Для реализации проекта используется Язык Python 3.11 и фреймворк FastAPI
- Авторизация и аутентификация пользователя происходит по JWT-token-у:
```python
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
```
- Роли пользователей определены в базе данных Postgresql 15.
- Вызов функций у клиента осуществляется при помощи Json-RPC 
```python
  #Method for get all users
@method
@app.get("/users", response_model=None)
def get_all_users(token:str) -> Result:   
    try:
        mapping_users_dto = MappingDTO()
        user_dto = jwtToken.verify_token(token)
        if user_dto.role == "admin" or user_dto.role == "user":
            users = mapping_users_dto.get_users_dto_from_db()
            return Success(users) 
        else:
            raise HTTPException(status_code=403, detail="Access Denied")    

    except PermissionError:
        raise InvalidTokenError(status_code=401, detail="Invalid token")
```

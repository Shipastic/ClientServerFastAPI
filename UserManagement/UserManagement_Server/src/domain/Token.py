from datetime import datetime, timedelta
from domain.Constants import *

class Token:
    def __init__(self, type, expire_at):
        self.type = type
        self.expire_at = expire_at
        self.token_lifetime = datetime.utcnow() +timedelta(expire_at)
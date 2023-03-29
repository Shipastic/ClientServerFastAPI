from datetime import datetime

class TokenDTO:
    user_id: int
    token: str
    created_at: datetime
    updated_at: datetime
    expires_at: datetime
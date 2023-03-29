import abc

class TokenRepository(abc.ABC):

    @abc.abstractmethod
    def get_refresh_token(self, username):
        pass

    @abc.abstractmethod
    def insert_refresh_token(self, id, refresh_token):
        pass

    @abc.abstractmethod
    def update_refresh_token(self, user_id, refresh_token):
        pass
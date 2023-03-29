import abc

class UserRepository(abc.ABC):

    @abc.abstractmethod
    def get_users(self):
        pass

    @abc.abstractmethod
    def get_user(self, username):
        pass

    @abc.abstractmethod
    def create_user(self, username, email, password):
        pass
    

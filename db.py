from user import User


class Memory:
    def __init__(self):
        self.users = {}

    def update_user(self, user: User):
        self.users[user.id] = user

    def get_user(self, id: str):
        return self.users[id]



class User:
    created_at: str
    first_name: str
    last_name: str
    email: str

    def __init__(self, created_at: str, first_name: str, last_name: str, email: str):
        self.created_at = created_at
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

    def get_user(self):
        return self

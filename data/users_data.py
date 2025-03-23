from faker import Faker

class User:
    fake = Faker()

    @staticmethod
    def create_user_data():
        return {
            "email": User.fake.email(),
            "password": User.fake.password(),
            "name": User.fake.name()
        }

    @staticmethod
    def get_static_user(email=None, password=None, name=None):
        return {
            "email": email or User.fake.email(),
            "password": password or User.fake.password(),
            "name": name or User.fake.name()
        }

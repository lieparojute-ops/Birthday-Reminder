class BirthdayManager:
    def __init__(self, repository, factory):
        self._users = []
        self._repository = repository
        self._factory = factory

    def add_user(self, user):
        for existing_user in self._users:
            if existing_user.username.lower() == user.username.lower():
                raise ValueError("This user already exists.")
        self._users.append(user)

    def remove_user(self, username):
        for user in self._users:
            if user.username.lower() == username.lower():
                self._users.remove(user)
                return
        raise ValueError("User not found.")

    def find_user(self, username):
        for user in self._users:
            if user.username.lower() == username.lower():
                return user
        raise ValueError("User not found.")

    def add_birthday_to_user(self, username, birthday):
        user = self.find_user(username)
        user.add_birthday(birthday)

    def remove_birthday_from_user(self, username, birthday_name):
        user = self.find_user(username)
        user.remove_birthday(birthday_name)

    def get_all_users(self):
        return self._users.copy()

    def save_data(self):
        self._repository.save_users(self._users)

    def load_data(self):
        self._users = self._repository.load_users()

    def send_all_today_notifications(self):
        for user in self._users:
            user.send_today_notifications(self._factory)
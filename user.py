from birthday import Birthday

class User:
    def __init__(self, username, email):
        self.username = username
        self.email = email
        self._birthdays = []

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Username cannot be empty.")
        self._username = value.strip()

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Email cannot be empty.")
        self._email = value.strip()

    @property
    def birthdays(self):
        return self._birthdays

    def add_birthday(self, birthday):
        if not isinstance(birthday, Birthday):
            raise TypeError("Expected a Birthday instance.")

        for existing_birthday in self._birthdays:
            if existing_birthday.name.lower() == birthday.name.lower():
                raise ValueError("This birthday already exists for this user.")

        self._birthdays.append(birthday)

    def remove_birthday(self, name):
        for birthday in self._birthdays:
            if birthday.name.lower() == name.lower():
                self._birthdays.remove(birthday)
                return
        raise ValueError("Birthday not found.")

    def get_all_birthdays(self):
        return sorted(self._birthdays, key=self._sort_by_days)

    def _sort_by_days(self, birthday):
        return birthday.days_until_birthday()

    def get_today_birthdays(self):
        return [birthday for birthday in self._birthdays
                if birthday.days_until_birthday() == 0
        ]

    def get_upcoming_birthdays(self, days=7):
        return [
            birthday
            for birthday in self._birthdays
            if 0 <= birthday.days_until_birthday() <= days
        ]

    def send_today_notifications(self, factory):
        today_birthdays = self.get_today_birthdays()

        for birthday in today_birthdays:
            notification = factory.create_notification(
                birthday.notification_type
            )
            notification.send(birthday)

    def __str__(self):
        return (
            f"User: {self.username}, "
            f"Email: {self.email}, "
            f"Birthdays count: {len(self._birthdays)}"
        )
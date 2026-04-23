
from datetime import date, datetime
from abc import ABC, abstractmethod


class Birthday:
    def __init__(self, name, birth_date, note="", notification_type="console"):
        self.name = name
        self.birth_date = birth_date
        self.note = note
        self.notification_type = notification_type

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Name cannot be empty.")
        self._name = value.strip()

    @property
    def birth_date(self):
        return self._birth_date

    @birth_date.setter
    def birth_date(self, value):
        try:
            self._birth_date = datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Birth date must be in YYYY-MM-DD format.")
        
        if self._birth_date > date.today():
            raise ValueError("Birth date cannot be in the future.")

    @property
    def notification_type(self):
        return self._notification_type

    @notification_type.setter
    def notification_type(self, value):
        if value not in ["email", "sms", "console"]:
            raise ValueError("Notification type must be 'email', 'sms', or 'console'.")
        self._notification_type = value

    def days_until_birthday(self):
        today = date.today()
        next_birthday = self._birth_date.replace(year=today.year)

        if next_birthday < today:
            next_birthday = next_birthday.replace(year=today.year + 1)

        return (next_birthday - today).days
    
    def get_reminder_text(self):
        days = self.days_until_birthday()

        if days == 0:
            message = f"Today is {self.name}'s birthday"
        elif days == 1:
            message = f"{self.name}'s birthday is tomorrow"
        else:
            message = f"{self.name}'s birthday is in {days} days"

        # Add note to message if it exists
        if self.note.strip():
            message += f" ({self.note})"

        return message

    def __str__(self):
        note_text = self.note if self.note.strip() else "No note"
        return (
            f"Name: {self._name}, "
            f"Birth date: {self._birth_date.strftime('%Y-%m-%d')}, "
            f"Notification type: {self.notification_type}, "
            f"Note: {note_text}"
        )


# User class

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

        # .lower() method ensures that entries like "Alice" and "alice" are treated as the same
        # This prevents duplicate entries for the same person with different capitalization

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
        return [birthday for birthday in self._birthdays if birthday.days_until_birthday() == 0]

    def get_upcoming_birthdays(self, days=7):
        return [
            birthday
            for birthday in self._birthdays
            if 0 <= birthday.days_until_birthday() <= days
        ]


# Notification system

class NotificationService(ABC):
    @abstractmethod
    def send(self, birthday):
        pass

class ConsoleNotification(NotificationService):
    def send(self, birthday):
        print(birthday.get_reminder_text())

class EmailNotification(NotificationService):
    def send(self, birthday):
        print(f"Sending email: {birthday.get_reminder_text()}")

class SMSNotification(NotificationService):
    def send(self, birthday):
        print(f"Sending SMS: {birthday.get_reminder_text()}")


# Factory pattern for creating notifications

class NotificationFactory:
    def create_notification(self, channel):
        if channel == "console":
            return ConsoleNotification()
        elif channel == "sms":
            return SMSNotification()
        elif channel == "email":
            return EmailNotification()
        else:
            raise ValueError("Unknown notification type")

# Test cases

def main():
    birthday = Birthday("Alice", "2006-04-30", notification_type="console")
    birthday_1 = Birthday("Bob", "1990-04-23", "Wish him a happy birthday!", "email")

    factory = NotificationFactory()

    print(birthday)
    notification_1 = factory.create_notification(birthday.notification_type)
    notification_1.send(birthday)

    print()

    print(birthday_1)
    notification_2 = factory.create_notification(birthday_1.notification_type)
    notification_2.send(birthday_1)


if __name__ == "__main__":
    main()

from datetime import date, datetime
from abc import ABC, abstractmethod
import csv


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

        # Add note to message if it exists (optional!!!)
        if self.note.strip():
            message += f" ({self.note})"

        return message

    def __str__(self):
        note_text = self.note if self.note.strip() else "No note"
        return (
            f"Name: {self.name}, "
            f"Birth date: {self.birth_date.strftime('%Y-%m-%d')}, "
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
        return [birthday for birthday in self._birthdays
                if birthday.days_until_birthday() == 0
        ]

    def get_upcoming_birthdays(self, days=7):
        return [
            birthday
            for birthday in self._birthdays
            if 0 <= birthday.days_until_birthday() <= days
        ]

# Function to send notifications for today's birthdays
# using factory to create notification based on birthday's notification type

    def send_today_notifications(self, factory):
        today_birthdays = self.get_today_birthdays()

        for birthday in today_birthdays:
            notification = factory.create_notification( # Creates notification object
                birthday.notification_type
            )
            notification.send(birthday) # Calls the correct send method depending on type

    def __str__(self):
        return (
            f"User: {self.username}, "
            f"Email: {self.email}, "
            f"Birthdays count: {len(self._birthdays)}" # Counts number of birthdays in the user's list
        )


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
        

# Repository for saving and loading user data to/from a CSV file
# encoding="utf-8" ensures that the file can handle a wide range of characters(eg. emojis) without causing encoding errors.

class CsvRepository:
    def __init__(self, file_name="user_data.csv"):
        self.file_path = file_name

    def save_users(self, users):
        with open(self.file_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            writer.writerow([
                "username",
                "email",
                "name",
                "birth_date",
                "note",
                "notification_type"
            ])

            for user in users:
                for birthday in user.birthdays:
                    writer.writerow([
                        user.username,
                        user.email,
                        birthday.name,
                        birthday.birth_date.strftime("%Y-%m-%d"),
                        birthday.note,
                        birthday.notification_type
                    ])

    def load_users(self):
        users = {}

        try:
            with open(self.file_path, "r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)

                for row in reader:
                    username = row["username"]
                    email = row["email"]

                    if username not in users:
                        users[username] = User(username, email)

                    birthday = Birthday(
                        row["name"],
                        row["birth_date"],
                        row["note"],
                        row["notification_type"]
                    )

                    users[username].add_birthday(birthday)

        except FileNotFoundError:
            return []

        return list(users.values())

# Test cases

def main():
    birthday = Birthday("Alice", "2006-04-30", notification_type="console")
    birthday_1 = Birthday("Bob", "1990-04-23", "Wish him a happy birthday!", "email")

    birthday_2 = Birthday("Tomas", "2001-12-05", "Cousin", "sms")

    user_1 = User("Mantas", "mantas@example.com")
    user_1.add_birthday(birthday)
    user_1.add_birthday(birthday_1)

    user_2 = User("Ema", "ema@example.com")
    user_2.add_birthday(birthday_2)

    users = [user_1, user_2]

    factory = NotificationFactory()
    repository = CsvRepository("user_data.csv") # the file will appear in the same folder as your Python file.

    # Save users to CSV
    repository.save_users(users) # If the file does not exist yet, Python creates it.
    print("Data saved to CSV.\n")


    # The load_users method opens the CSV file, reads rows, recreates User objects
    # recreates Birthday objects, returns a list of users.
    loaded_users = repository.load_users()

    print("Loaded users from CSV:")
    for user in loaded_users:
        print(user)
        print()

        print("All birthdays:")
        for item in user.get_all_birthdays():
            print(item)

        print()
        print("Upcoming reminders:")
        for item in user.get_upcoming_birthdays(30):
            print(item.get_reminder_text())

        print()
        print("Today's notifications:")
        user.send_today_notifications(factory)
        print("-" * 40)


if __name__ == "__main__":
    main()


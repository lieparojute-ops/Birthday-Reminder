from abc import ABC, abstractmethod
import csv
from datetime import date, datetime


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
            raise ValueError(
                "Notification type must be 'email', 'sms', or 'console'."
            )
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
        return self._users

    def save_data(self):
        self._repository.save_users(self._users)

    def load_data(self):
        self._users = self._repository.load_users()

    def send_all_today_notifications(self):
        for user in self._users:
            user.send_today_notifications(self._factory)


class Menu:
    def __init__(self, manager):
        self.manager = manager

    def display_menu(self):
        print("\n--- Birthday Reminder Menu ---")
        print("1. View all users and birthdays")
        print("2. Add birthday")
        print("3. Remove birthday")
        print("4. View upcoming reminders")
        print("5. Send today's notifications")
        print("6. Save and exit")

    def run(self):
        while True:
            self.display_menu()
            choice = input("Choose an option: ")

            if choice == "1":
                self.handle_show_all()

            elif choice == "2":
                self.handle_add_birthday()

            elif choice == "3":
                self.handle_remove_birthday()

            elif choice == "4":
                self.handle_show_reminders()

            elif choice == "5":
                self.manager.send_all_today_notifications()

            elif choice == "6":
                self.manager.save_data()
                print("Data saved. Goodbye!")
                break

            else:
                print("Invalid option. Please try again.")

    def handle_show_all(self):
        for user in self.manager.get_all_users():
            print(user)
            for birthday in user.get_all_birthdays():
                print(" ", birthday)

    def handle_add_birthday(self):
        username = input("Enter username: ")
        name = input("Enter birthday person's name: ")
        birth_date = input("Enter birth date (YYYY-MM-DD): ")
        note = input("Enter note (optional): ")
        notification_type = input("Notification type (console/email/sms): ")

        try:
            birthday = Birthday(name, birth_date, note, notification_type)
            self.manager.add_birthday_to_user(username, birthday)
            print("Birthday added.")
        except ValueError as error:
            print(f"Error: {error}")

    def handle_remove_birthday(self):
        username = input("Enter username: ")
        name = input("Enter birthday person's name to remove: ")

        try:
            self.manager.remove_birthday_from_user(username, name)
            print("Birthday removed.")
        except ValueError as error:
            print(f"Error: {error}")

    def handle_show_reminders(self):
        for user in self.manager.get_all_users():
            print(f"\nReminders for {user.username}:")
            for birthday in user.get_upcoming_birthdays(30):
                print(birthday.get_reminder_text())


def main():
    repository = CsvRepository("user_data.csv")
    factory = NotificationFactory()
    manager = BirthdayManager(repository, factory)

    manager.load_data()

    if not manager.get_all_users():
        user_1 = User("Mantas", "mantas.tj@gmail.com")
        user_2 = User("Ema", "ema.baltusyte@gmail.com")

        manager.add_user(user_1)
        manager.add_user(user_2)

        manager.add_birthday_to_user(
            "Mantas",
            Birthday("Alice", "2006-04-30", notification_type="console")
        )
        manager.add_birthday_to_user(
            "Mantas",
            Birthday("Bob", "1990-05-15", "Send a birthday card!", "email")
        )
        manager.add_birthday_to_user(
            "Ema",
            Birthday("Monika", "2001-05-20", "Buy a cake", "sms")
        )

        manager.save_data()

    menu = Menu(manager)
    menu.run()


if __name__ == "__main__":
    main()
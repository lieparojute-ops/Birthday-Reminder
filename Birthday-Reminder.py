
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
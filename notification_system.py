from abc import ABC, abstractmethod


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
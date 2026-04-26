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
    def __init__(self):
        self._notification_types = {
            "console": ConsoleNotification,
            "sms": SMSNotification,
            "email": EmailNotification
        }

    def create_notification(self, channel):
        try:
            return self._notification_types[channel]()
        except KeyError:
            raise ValueError("Unknown notification type")
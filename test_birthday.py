import os
import unittest

from birthday import Birthday
from user import User
from csv_repository import CsvRepository
from notification_system import NotificationFactory, ConsoleNotification
from manager import BirthdayManager


class TestBirthday(unittest.TestCase):

    def test_valid_birthday(self):
        b = Birthday("Alice", "2000-01-01")
        self.assertEqual(b.name, "Alice")

    def test_invalid_date(self):
        with self.assertRaises(ValueError):
            Birthday("Alice", "wrong-date")

    def test_future_date(self):
        with self.assertRaises(ValueError):
            Birthday("Alice", "3000-01-01")

    def test_days_until(self):
        b = Birthday("Test", "2000-01-01")
        self.assertIsInstance(b.days_until_birthday(), int)


class TestUser(unittest.TestCase):

    def setUp(self):
        self.user = User("TestUser", "test@email.com")
        self.birthday = Birthday("Alice", "2000-01-01")

    def test_add_birthday(self):
        self.user.add_birthday(self.birthday)
        self.assertEqual(len(self.user.birthdays), 1)

    def test_duplicate_birthday(self):
        self.user.add_birthday(self.birthday)
        with self.assertRaises(ValueError):
            self.user.add_birthday(self.birthday)

    def test_remove_birthday(self):
        self.user.add_birthday(self.birthday)
        self.user.remove_birthday("Alice")
        self.assertEqual(len(self.user.birthdays), 0)

    def test_invalid_email(self):
        with self.assertRaises(ValueError):
            User("TestUser", "invalid-email")


class TestRepository(unittest.TestCase):

    def tearDown(self):
        if os.path.exists("test_data.csv"):
            os.remove("test_data.csv")

    def test_save_and_load(self):
        repo = CsvRepository("test_data.csv")

        user = User("TestUser", "test@email.com")
        user.add_birthday(Birthday("Alice", "2000-01-01"))

        repo.save_users([user])
        loaded_users = repo.load_users()

        self.assertEqual(len(loaded_users), 1)
        self.assertEqual(len(loaded_users[0].birthdays), 1)
        self.assertEqual(loaded_users[0].username, "TestUser")
        self.assertEqual(loaded_users[0].birthdays[0].name, "Alice")
        self.assertEqual(
            loaded_users[0].birthdays[0].birth_date.strftime("%Y-%m-%d"),
            "2000-01-01"
        )

    def test_save_and_load_user_without_birthdays(self):
        repo = CsvRepository("test_data.csv")

        user = User("EmptyUser", "empty@email.com")

        repo.save_users([user])
        loaded_users = repo.load_users()

        self.assertEqual(len(loaded_users), 1)
        self.assertEqual(loaded_users[0].username, "EmptyUser")
        self.assertEqual(len(loaded_users[0].birthdays), 0)


class TestNotificationFactory(unittest.TestCase):

    def test_invalid_notification_type(self):
        factory = NotificationFactory()
        with self.assertRaises(ValueError):
            factory.create_notification("invalid-type")

    def test_create_console_notification(self):
        factory = NotificationFactory()
        notification = factory.create_notification("console")
        self.assertIsInstance(notification, ConsoleNotification)

    def test_reminder_text_contains_name(self):
        birthday = Birthday("Alice", "2000-01-01", "Friend")
        text = birthday.get_reminder_text()
        self.assertIn("Alice", text)
        self.assertIn("Friend", text)


class TestBirthdayManager(unittest.TestCase):

    def setUp(self):
        self.repo = CsvRepository("test_data.csv")
        self.factory = NotificationFactory()
        self.manager = BirthdayManager(self.repo, self.factory)

    def test_add_and_find_user(self):
        user = User("TestUser", "test@email.com")
        self.manager.add_user(user)

        found_user = self.manager.find_user("TestUser")
        self.assertEqual(found_user.username, "TestUser")

    def test_duplicate_user(self):
        user_1 = User("TestUser", "test@email.com")
        user_2 = User("testuser", "other@email.com")

        self.manager.add_user(user_1)

        with self.assertRaises(ValueError):
            self.manager.add_user(user_2)

    def test_remove_missing_user(self):
        with self.assertRaises(ValueError):
            self.manager.remove_user("Unknown")

    def test_add_birthday_to_user(self):
        user = User("TestUser", "test@email.com")
        birthday = Birthday("Alice", "2000-01-01")

        self.manager.add_user(user)
        self.manager.add_birthday_to_user("TestUser", birthday)

        self.assertEqual(len(user.birthdays), 1)


if __name__ == "__main__":
    unittest.main()

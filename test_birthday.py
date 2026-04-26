import os
import unittest

from birthday_reminder import (
    Birthday,
    User,
    CsvRepository,
    NotificationFactory,
    ConsoleNotification,
    BirthdayManager,
)


class TestBirthday(unittest.TestCase):

    def test_valid_birthday(self):
        b = Birthday("Alice", "2000-01-01")
        self.assertEqual(b.name, "Alice")

    def test_invalid_date(self):
        with self.assertRaises(ValueError): # Check that creating a birthday with an invalid date raises an error
            Birthday("Alice", "wrong-date")

    def test_future_date(self):
        with self.assertRaises(ValueError): # Check that creating a birthday with a future date raises an error
            Birthday("Alice", "3000-01-01")

    def test_days_until(self):
        b = Birthday("Test", "2000-01-01")
        self.assertIsInstance(b.days_until_birthday(), int) # Check that the days_until_birthday method returns an integer


class TestUser(unittest.TestCase):

    def setUp(self):
        self.user = User("TestUser", "test@email.com")
        self.birthday = Birthday("Alice", "2000-01-01")

    def test_add_birthday(self):
        self.user.add_birthday(self.birthday)
        self.assertEqual(len(self.user.birthdays), 1) # Check that the birthday was added to the user's list of birthdays

    def test_duplicate_birthday(self):
        self.user.add_birthday(self.birthday)
        with self.assertRaises(ValueError): # Check that adding a duplicate birthday raises an error
            self.user.add_birthday(self.birthday)

    def test_remove_birthday(self):
        self.user.add_birthday(self.birthday)
        self.user.remove_birthday("Alice")
        self.assertEqual(len(self.user.birthdays), 0)


class TestRepository(unittest.TestCase):

    def tearDown(self):
        if os.path.exists("test_data.csv"): # Clean up the test data file after each test
            os.remove("test_data.csv")

    def test_save_and_load(self):
        repo = CsvRepository("test_data.csv")

        user = User("TestUser", "test@email.com")
        user.add_birthday(Birthday("Alice", "2000-01-01"))

        repo.save_users([user])
        loaded_users = repo.load_users()

        self.assertEqual(len(loaded_users), 1)  # Check that one user was loaded from the file
        self.assertEqual(len(loaded_users[0].birthdays), 1) # Check that the loaded user has one birthday
        self.assertEqual(loaded_users[0].username, "TestUser") # Check that the loaded user's username is correct
        self.assertEqual(loaded_users[0].birthdays[0].name, "Alice") # Check that the loaded birthday's name is correct
        self.assertEqual(loaded_users[0].birthdays[0].birth_date.strftime("%Y-%m-%d"),"2000-01-01") # Check that the loaded birthday's date is correct


class TestNotificationFactory(unittest.TestCase):

    def test_invalid_notification_type(self):
        factory = NotificationFactory()
        with self.assertRaises(ValueError):
            factory.create_notification("invalid-type") # Check that creating a notification with an invalid type raises an error

    def test_create_console_notification(self):
        factory = NotificationFactory()
        notification = factory.create_notification("console")
        self.assertIsInstance(notification, ConsoleNotification) # Check that the created notification is of the correct type

    def test_reminder_text_contains_name(self):
        birthday = Birthday("Alice", "2000-01-01", "Friend")
        text = birthday.get_reminder_text()
        self.assertIn("Alice", text) # Check that the reminder text contains the name of the person
        self.assertIn("Friend", text) # Check that the reminder text contains the relationship if provided


class TestBirthdayManager(unittest.TestCase):

    def test_add_and_find_user(self):
        repo = CsvRepository("test_data.csv") # Use a test data file for the repository to avoid affecting real data
        factory = NotificationFactory()
        manager = BirthdayManager(repo, factory)

        user = User("TestUser", "test@email.com")
        manager.add_user(user) # Add a user to the manager and check that it can be found

        found_user = manager.find_user("TestUser")
        self.assertEqual(found_user.username, "TestUser") # Check that the found user's username is correct

    def test_add_birthday_to_user(self):
        repo = CsvRepository("test_data.csv")
        factory = NotificationFactory()
        manager = BirthdayManager(repo, factory)

        user = User("TestUser", "test@email.com")
        birthday = Birthday("Alice", "2000-01-01")

        manager.add_user(user)
        manager.add_birthday_to_user("TestUser", birthday)

        self.assertEqual(len(user.birthdays), 1) # Check that the birthday was added to the user's list of birthdays


if __name__ == "__main__":
    unittest.main()
import unittest
from Birthday-Reminder import Birthday, User, CsvRepository


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


class TestRepository(unittest.TestCase):

    def test_save_and_load(self):
        repo = CsvRepository("test_data.csv")

        user = User("TestUser", "test@email.com")
        user.add_birthday(Birthday("Alice", "2000-01-01"))

        repo.save_users([user])
        loaded_users = repo.load_users()

        self.assertEqual(len(loaded_users), 1)
        self.assertEqual(len(loaded_users[0].birthdays), 1)


if __name__ == "__main__":
    unittest.main()
import csv
from birthday import Birthday
from user import User

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
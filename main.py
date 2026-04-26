from notification import NotificationFactory
from repository import CsvRepository
from manager import BirthdayManager
from menu import Menu

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
from notification_system import NotificationFactory
from csv_repository import CsvRepository
from manager import BirthdayManager
from menu import Menu


def main():
    repository = CsvRepository("user_data.csv")
    factory = NotificationFactory()
    manager = BirthdayManager(repository, factory)

    manager.load_data()

    menu = Menu(manager)
    menu.run()


if __name__ == "__main__":
    main()
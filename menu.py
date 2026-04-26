from birthday import Birthday


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
        
        if not notification_type:
            notification_type = "console"

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
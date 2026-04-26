# Birthday reminder system

## 1. Introduction

### What is this system?

This project is a **Birthday Reminder system** developed using Object-Oriented Programming (OOP) principles in Python. The system allows users to store and manage birthdays, receive reminders, and persist data between program runs.

### How to run the program

1. Make sure Python is installed.
2. Open the project folder.
3. Run the program using:

   ```bash
   python main.py
   ```

### How to use the program

* Add users with email addresses
* Add birthdays for each user
* View all stored birthdays
* View upcoming reminders
* Send notifications for today’s birthdays
* Save data to file before exiting

The program uses a console-based menu system for interaction.

---

### Project Structure

- birthday.py – Birthday class and logic  
- user.py – User management  
- manager.py – Main system logic  
- csv_repository.py – File handling  
- notification_system.py – Notifications and factory  
- menu.py – User interface  
- test_birthday.py – Unit tests

---

## 2. Body / Analysis

### Functional Requirements Implementation

The application fully implements the Birthday Reminder system requirements:

* Add/remove birthdays – implemented in BirthdayManager methods such as add_birthday_to_user() and remove_birthday_from_user()
* Print birthday reminders – implemented using Birthday.get_reminder_text() and Menu display
* Save data to a file (CSV) – implemented in CsvRepository.save_users()
* Send notifications – implemented using NotificationFactory and send_today_notifications()
* Support multiple users – handled through BirthdayManager user list

These are handled through a modular system consisting of classes such as `User`, `Birthday`, `BirthdayManager`, and `CsvRepository`.

---

### OOP Principles

#### Encapsulation

Encapsulation is used by protecting internal data with private attributes and exposing them through properties.

Example:

```python
@property
def birthdays(self):
    return self._birthdays.copy()
```

This prevents external modification of internal state.

---

#### Abstraction

Abstraction is implemented using an abstract base class:

```python
class NotificationService(ABC):
    @abstractmethod
    def send(self, birthday):
        pass
```

This defines a common interface for all notification types.

---

#### Inheritance

Notification classes inherit from the abstract base class:

```python
class EmailNotification(NotificationService):
```

This allows reuse of structure while implementing different behavior.

---

#### Polymorphism

Different notification types implement the same method:

```python
notification.send(birthday)
```

Each class behaves differently, but they are used through a common interface.

---

### Design Pattern

The application uses the **Factory Method pattern**:

The factory stores available notification types in a dictionary and creates the correct object dynamically based on the selected type.

```python
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
```

It creates notification objects based on type (console, email, sms).

This pattern was chosen because:

* It separates object creation from usage
* It allows easy extension of new notification types
* It improves flexibility and maintainability

Compared to using conditional statements (if/else), the Factory Method pattern provides a more scalable and maintainable way to create objects.

---

### Composition / Aggregation

* A `User` contains multiple `Birthday` objects → **composition**
* `BirthdayManager` manages users, repository, and notifications → **aggregation**

This structure keeps responsibilities clearly separated.

---

### File Handling

The system uses a CSV file to store user and birthday data. File operations are implemented in the `CsvRepository` class.

Data is written to the file using the `save_users()` method. Each user and their birthdays are saved. Users without birthdays are also stored to prevent data loss.

```python
for user in users:
    if not user.birthdays:
        writer.writerow([user.username, user.email, "", "", "", ""])
    else:
        for birthday in user.birthdays:
            writer.writerow([
                user.username,
                birthday.name,
                birthday.birth_date.strftime("%Y-%m-%d")
            ])
```

Data is loaded from the file using the `load_users` method. The system recreates users and only creates birthday objects when data exists.

```python
if username not in users:
    users[username] = User(username, email)

if row["name"] and row["birth_date"]:
    birthday = Birthday(row["name"], row["birth_date"])
    users[username].add_birthday(birthday)
```

This ensures that all user data is preserved between program executions.

---

### Error Handling

The program uses exceptions (such as ValueError) to validate user input and prevent invalid data from being processed. This ensures that incorrect values (e.g., invalid dates or emails) are handled safely and do not break the program.

---

### Testing

The application includes unit tests using the `unittest` framework.

Test coverage includes:

* Birthday validation
* User operations
* Repository save/load
* Notification factory
* Manager logic

Example:

```python
with self.assertRaises(ValueError):
    manager.add_user(user_2)
```

---

## 3. Results

* The application successfully manages multiple users and birthdays
* File persistence ensures data is not lost between runs
* OOP principles improve code structure and maintainability
* One challenge was handling edge cases such as duplicate users and empty data
* Another challenge was ensuring proper validation and error handling

---

## 4. Conclusions

This project demonstrates the practical application of OOP principles in Python.

The result is a modular and extendable system that:

* Manages birthdays efficiently
* Supports multiple users
* Provides flexible notification handling

Future improvements could include:

* GUI interface instead of console menu
* Real email/SMS integration
* Database instead of CSV storage
* Additional notification types

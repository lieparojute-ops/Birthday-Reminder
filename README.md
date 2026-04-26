# Birthday-Reminder

# Birthday Reminder Application

## 1. Introduction

### What is this application?

This project is a **Birthday Reminder system** developed using Object-Oriented Programming (OOP) principles in Python. The application allows users to store and manage birthdays, receive reminders, and persist data between program runs.

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

## 2. Body / Analysis

### Functional Requirements Implementation

The application fully implements the Birthday Reminder system requirements:

* Add/remove birthdays
* Print birthday reminders
* Save data to a file (CSV)
* Send notifications on the birthday
* Support multiple users

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

---

### Composition / Aggregation

* A `User` contains multiple `Birthday` objects → **composition**
* `BirthdayManager` manages users, repository, and notifications → **aggregation**

This structure keeps responsibilities clearly separated.

---

### File Handling

The system uses a CSV file to store user and birthday data.

Data is written to the file using the `save_users()` method:

```python
def save_users(self, users):
    writer.writerow([
        user.username,
        user.email,
        birthday.name,
        birthday.birth_date.strftime("%Y-%m-%d"),
        birthday.note,
        birthday.notification_type
    ])
```

Data is loaded from the file using the `load_users` method:

```python
if row["name"] and row["birth_date"]:
    birthday = Birthday(
        row["name"],
        row["birth_date"],
        row["note"],
        row["notification_type"] or "console"
    )
    users[username].add_birthday(birthday)
```

This ensures that user data persists between program executions.

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

# Birthday Reminder System

## 1. Introduction

### 1.1 Purpose of the System

The **Birthday Reminder System** is a multi-user, console-based Python application using Object-Oriented Programming (OOP) principles. The purpose of the system is to allow users to manage and store birthday records, view upcoming birthdays, save and load data from a CSV file, and simulate notifications on the day of a birthday.

### 1.2 Application

The application supports the main birthday reminder requirements:

* Building a program to remind birthdays
* Adding and removing birthdays
* Printing birthday reminders
* Saving birthdays to a file
* Sending notifications on the day of the birthday
* Supporting multiple users

### 1.3 How to Run the Program

Run the application from the project folder with:

```bash
python main.py
```

### 1.4 How to Use the Program

After running `main.py`, the console menu is displayed:

```text
--- Birthday Reminder Menu ---
1. View all users and birthdays
2. Add user
3. Remove user
4. Add birthday
5. Remove birthday
6. View upcoming reminders
7. Send today's notifications
8. Save and exit
```

Typical usage flow:

1. Add a user by entering a username and email address.
2. Add one or more birthdays for that user.
3. Choose a notification type: `console`, `email`, or `sms`.
4. View all stored users and birthdays.
5. View upcoming reminders.
6. Send today's birthday notifications.
7. Save the data and exit.

Data is stored in `user_data.csv` when the user selects **Save and exit**.

---

## 2. Body / Analysis

### 2.1 Project Structure

The system is divided into separate modules. Each module has a focused responsibility:

| File | Responsibility |
|---|---|
| `main.py` | Starts the application and connects the main objects. |
| `menu.py` | Handles console input and output. |
| `manager.py` | Controls the main application logic. |
| `birthday.py` | Represents birthday data and birthday-related calculations. |
| `user.py` | Represents a user and manages that user's birthdays. |
| `csv_repository.py` | Saves and loads user and birthday data from a CSV file. |
| `notification_system.py` | Defines notification services and notification object creation. |
| `test_birthday.py` | Contains unit tests for core functionality. |

### 2.2 Functional Requirements Implementation

#### Add and Remove Birthdays

Birthday records are created using the `Birthday` class and added to a user through the `User` and `BirthdayManager` classes.

```python
def add_birthday_to_user(self, username, birthday):
    user = self.find_user(username)
    user.add_birthday(birthday)
```

Removing a birthday is also handled through the manager layer:

```python
def remove_birthday_from_user(self, username, birthday_name):
    user = self.find_user(username)
    user.remove_birthday(birthday_name)
```

#### Print Birthday Reminders

The `Birthday` class calculates how many days remain until the next birthday and returns a readable reminder message.

```python
def get_reminder_text(self):
    days = self.days_until_birthday()

    if days == 0:
        message = f"Today is {self.name}'s birthday"
    elif days == 1:
        message = f"{self.name}'s birthday is tomorrow"
    else:
        message = f"{self.name}'s birthday is in {days} days"
```

Upcoming reminders are displayed through the menu by using each user's `get_upcoming_birthdays()` method.

#### Save Birthdays to File

The `CsvRepository` class handles writing users and birthdays to a CSV file.

```python
def save_users(self, users):
    with open(self.file_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
```

Each row stores the username, email, birthday name, birth date, note, and notification type.

#### Load Birthdays from File

The same repository class reads saved CSV data and reconstructs `User` and `Birthday` objects.

```python
def load_users(self):
    users = {}
```

If the file does not exist yet, the program returns an empty list instead of crashing.

#### Send Notifications on the Day of the Birthday

The `User` class checks birthdays that occur today. For each birthday, it asks the notification factory to create the correct notification object.

```python
def send_today_notifications(self, factory):
    today_birthdays = self.get_today_birthdays()

    for birthday in today_birthdays:
        notification = factory.create_notification(
            birthday.notification_type
        )
        notification.send(birthday)
```

#### Support Multiple Users

The `BirthdayManager` stores multiple users in the `_users` list and prevents duplicate usernames by comparing usernames case-insensitively.

```python
def add_user(self, user):
    for existing_user in self._users:
        if existing_user.username.lower() == user.username.lower():
            raise ValueError("This user already exists.")
    self._users.append(user)
```

Each `User` object can store multiple `Birthday` objects.

---

## 2.3 Object-Oriented Programming Principles

### Encapsulation

Encapsulation means keeping object data protected and controlling access to it through methods or properties. In this project, internal attributes use a leading underscore, and validation is performed through property setters.

Example from `Birthday`:

```python
@property
def name(self):
    return self._name

@name.setter
def name(self, value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError("Name cannot be empty.")
    self._name = value.strip()
```

The `User` class also protects the internal birthday list by returning a copy instead of the original list:

```python
@property
def birthdays(self):
    return self._birthdays.copy()
```

This prevents external code from directly changing the internal state of the object.

### Abstraction

Abstraction means exposing a simple interface while hiding implementation details. The notification system uses an abstract base class to define the common interface for all notification types.

```python
class NotificationService(ABC):
    @abstractmethod
    def send(self, birthday):
        pass
```

The rest of the program can work with notification objects through the shared `send()` method without needing to know the exact notification class.

### Inheritance

Inheritance allows child classes to reuse and specialize behavior from a parent class. In this project, `ConsoleNotification`, `EmailNotification`, and `SMSNotification` inherit from `NotificationService`.

```python
class ConsoleNotification(NotificationService):
    def send(self, birthday):
        print(birthday.get_reminder_text())
```

Each subclass follows the same interface but provides its own implementation of `send()`.

### Polymorphism

Polymorphism means that objects of different classes can be used through the same interface. The notification classes all implement `send()`, but each class behaves differently.

```python
notification = factory.create_notification(birthday.notification_type)
notification.send(birthday)
```

The program does not need an `if` statement to decide how to send every notification. It only calls `send()`, and the correct behavior depends on the concrete notification object.

---

## 2.4 Composition and Aggregation

The project uses object relationships to connect classes together.

### User and Birthday Relationship

A `User` object stores a list of `Birthday` objects:

```python
self._birthdays = []
```

This is a composition-like relationship in the application context because birthdays are managed as part of a user. Each user can have multiple birthday records, and birthday operations are accessed through the user or manager.

### Manager, Repository, and Factory Relationship

`BirthdayManager` receives a repository and notification factory object:

```python
def __init__(self, repository, factory):
    self._users = []
    self._repository = repository
    self._factory = factory
```

This is aggregation/dependency injection because the manager uses these objects but does not create them directly. This improves flexibility and makes the manager easier to test.

---

## 2.5 Design Pattern

### Factory Method Pattern

The project implements the **Factory Method** pattern in `NotificationFactory`.

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

The Factory Method pattern enables dynamic creation of notification objects while keeping the system loosely coupled. It centralizes object creation, avoids conditional logic, and supports extensibility in line with the Open/Closed Principle.

Other design patterns were considered. The Singleton pattern is not appropriate because the system requires multiple independent notification objects rather than a single shared instance. The Strategy pattern could be used to switch behaviors at runtime, but it focuses on behavior selection rather than object creation. Since the primary concern in this system is flexible and extensible object creation, the Factory Method pattern is the most suitable choice.

---

## 2.6 Exception Handling and Validation

The system validates user input and raises clear exceptions when data is invalid.

Examples:

* Empty names are rejected.
* Birth dates must use `YYYY-MM-DD` format.
* Future birth dates are rejected.
* Email addresses must contain `@` and `.`.
* Duplicate users and duplicate birthdays are rejected.
* Missing CSV files are handled smoothly.

Example from `Birthday`:

```python
try:
    self._birth_date = datetime.strptime(value, "%Y-%m-%d").date()
except ValueError:
    raise ValueError("Birth date must be in YYYY-MM-DD format.")
```

The menu catches `ValueError` exceptions and prints user-friendly error messages instead of stopping the program.

---

## 2.7 Testing

Unit tests are implemented with Python's `unittest` framework in `test_birthday.py`.

The tests cover:

* Valid birthday creation
* Invalid date format handling
* Future date rejection
* Birthday reminder calculation
* Adding and removing birthdays
* Duplicate birthday detection
* Invalid email validation
* CSV save and load functionality
* Saving and loading users without birthdays
* Notification factory object creation
* Invalid notification type handling
* Birthday manager user operations

---

## 2.8 Code Style

The program is written in Python and follows PEP 8 style:

* Class names use `PascalCase`, for example `BirthdayManager` and `CsvRepository`.
* Function and variable names use `snake_case`, for example `add_birthday_to_user()`.
* Modules are separated by responsibility.
* The `if __name__ == "__main__":` guard is used in `main.py` and `test_birthday.py`.
* Validation and business logic are separated from console menu handling.

---

## 3. Results and Summary

* The system successfully implements a console-based birthday reminder application using Python and Object-Oriented Programming principles.
* All functional requirements are met, including managing multiple users, adding/removing birthdays, displaying reminders, sending notifications, and persisting data in CSV format.
* All four OOP pillars are demonstrated, and the Factory Method pattern provides a flexible notification system.
* Unit testing confirms the correctness of core functionality, including validation, data persistence, notification creation, and manager operations.
* One challenge was designing a flexible notification system while keeping the code loosely coupled, which was addressed using the Factory Method pattern.

---

## 4. Conclusions

This system successfully achieved its goal of developing a functional Python application that applies Object-Oriented Programming principles. The program allows users to manage birthday records, store data persistently, display reminders, and simulate notifications for upcoming events.

A key outcome is the clear separation of responsibilities between components, including user interaction, business logic, data storage, and notification handling. This modular structure improves readability, maintainability, and extensibility of the system.

Future improvements could include real notification integration (email/SMS), a graphical user interface, database storage, user authentication, configurable reminders, and automated scheduling.

Overall, the project satisfies all requirements and provides a solid foundation for further development.

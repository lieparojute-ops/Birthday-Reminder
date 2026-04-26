# Birthday Reminder System

## 1. Introduction

### 1.1 Purpose of the System

The Birthday Reminder System is a multi-user, console-based application developed in Python using Object-Oriented Programming (OOP) principles. The purpose of the system is to allow users to manage birthday records, store them persistently in a file, view upcoming birthdays, and receive notifications when a birthday occurs.

### 1.2 Functional Overview

The system provides the following functionality:

* Add and remove users
* Assign multiple birthdays to each user
* View all stored birthdays
* Display upcoming birthday reminders
* Send notifications for birthdays occurring today
* Save and load data using CSV files

### 1.3 Program Execution

The program is started by running:

```bash
python main.py
```

Execution flow:

1. The system initializes repository, notification factory, and manager
2. Stored data is loaded from a CSV file
3. A console menu is displayed
4. The user interacts with the system via menu options
5. Actions are processed through the manager layer
6. Notifications are generated if required
7. Data is saved before program termination

---

## 2. System Architecture

### 2.1 Main Components

The system is divided into modular components:

* `Birthday` – represents birthday data and logic
* `User` – manages user information and associated birthdays
* `BirthdayManager` – controls application logic
* `CsvRepository` – handles data persistence
* `NotificationFactory` – creates notification objects
* `Menu` – provides user interface

### 2.2 Design Structure

The architecture follows a layered approach:

* Presentation Layer → Menu
* Business Logic Layer → Manager, User, Birthday
* Data Layer → CSV Repository
* Service Layer → Notification System

This separation improves maintainability and readability.

---

## 3. Functional Requirements Implementation

The system satisfies all core requirements:

### 3.1 Birthday Management

* Adding/removing birthdays is handled by `BirthdayManager`
* Validation ensures no duplicates per user

### 3.2 Data Persistence

* Data is stored in CSV format via `CsvRepository`
* Users and birthdays are reconstructed during loading

### 3.3 Notifications

* Notifications are generated for birthdays occurring today
* Different notification types are supported (console, email, SMS)

### 3.4 Multi-user Support

* Each user can have multiple associated birthdays
* Users are uniquely identified by username

---

## 4. Object-Oriented Programming Principles

### 4.1 Encapsulation

Encapsulation is implemented by restricting direct access to class attributes and exposing them through properties.

Example:

```python
@property
def birthdays(self):
    return self._birthdays.copy()
```

This prevents unintended modification of internal state.

---

### 4.2 Abstraction

Abstraction is achieved using an abstract base class:

```python
class NotificationService(ABC):
    @abstractmethod
    def send(self, birthday):
        pass
```

Concrete implementations (Console, Email, SMS) define specific behavior while sharing a common interface.

---

### 4.3 Composition

Composition is used where a `User` object contains multiple `Birthday` objects.

* A user *owns* its birthdays
* Birthdays cannot exist independently in the system context

This models real-world relationships accurately.

---

### 4.4 Polymorphism

Polymorphism is demonstrated through the notification system:

* All notification types implement the same `send()` method
* Different behaviors are executed depending on the object type

---

### 4.5 SOLID Principles

The system follows several SOLID principles:

* **Single Responsibility Principle (SRP)**  
  Each class has a single, clearly defined responsibility.  
  For example, `CsvRepository` handles only data storage, while `BirthdayManager` handles application logic.

* **Open/Closed Principle (OCP)**  
  The system is open for extension but closed for modification.  
  New notification types can be added without modifying existing classes.

* **Liskov Substitution Principle (LSP)**  
  All notification types (Console, Email, SMS) can be used interchangeably through the `NotificationService` interface without affecting correctness.

* **Dependency Inversion Principle (DIP)**  
  High-level modules such as `BirthdayManager` depend on abstractions (repository and factory) rather than concrete implementations.

---

### 4.6 Inheritance

Inheritance is used in the notification system, where concrete notification classes inherit from the abstract base class `NotificationService`.

This allows shared structure and behavior to be defined once, while enabling specialized implementations in subclasses.

For example:
- `ConsoleNotification`
- `EmailNotification`
- `SMSNotification`

All of these classes inherit from `NotificationService` and implement the `send()` method.

This promotes code reuse, consistency, and extensibility.

---

## 5. Design Patterns

### 5.1 Factory Pattern

The system implements the Factory Method pattern through the `NotificationFactory` class.

The purpose of this pattern is to create notification objects dynamically based on a specified type (e.g., email, SMS, console), without exposing the object creation logic to the client code.

Example:

```python
factory.create_notification("email")
```

This pattern is particularly suitable in this system because multiple notification types share a common interface but differ in behavior.

In scenarios where different types of notification objects with varying behaviours and characteristics are required, the Factory Pattern provides a flexible and scalable solution.

Compared to directly instantiating objects, this approach:

Reduces coupling between classes
Centralizes object creation logic
Allows easy addition of new notification types without modifying existing code

Alternative patterns such as the Singleton Pattern would not be suitable here, as the system requires multiple interchangeable notification objects rather than a single shared instance.

---

## 6. Exception Handling

The system includes validation and error handling:

* Invalid date formats are rejected
* Future birth dates are not allowed
* Invalid email formats raise errors
* Duplicate entries are prevented
* Missing files are handled smoothly

This ensures robustness and reliability.

---

## 7. Testing

Unit tests are implemented using the `unittest` framework.

Test coverage includes:

* Birthday validation
* User operations (add/remove)
* Duplicate detection
* Repository save/load functionality

Example:

```python
with self.assertRaises(ValueError):
    Birthday("Alice", "wrong-date")
```

Testing ensures correctness and reduces bugs.

---

## 8. Example Usage

Example interaction:

```
--- Birthday Reminder Menu ---
1. Add user
2. Add birthday

Enter username: John
Enter email: john@email.com

Enter birthday name: Alice
Enter birth date: 2000-01-01

Upcoming reminder:
Alice's birthday is in 5 days
```

Example notification:

```
Sending email: Today is Alice's birthday!
```

---

## 9. Limitations

* No graphical user interface (CLI only)
* Email and SMS notifications are simulated
* Data storage is limited to CSV format
* No authentication system

---

## 10. Possible Improvements

* Implement real email/SMS integration
* Add graphical user interface (GUI)
* Use database instead of CSV
* Add authentication and user roles
* Extend notification scheduling

---

## 11. Results

- The system successfully implements a multi-user birthday reminder application using OOP principles  
- Functional requirements such as data persistence, notifications, and user management were fully achieved  
- One challenge was designing a flexible notification system, which was solved using the Factory pattern  
- Input validation and error handling improved system robustness  
- Unit testing ensured reliability of core functionality

---

## 12. Conclusion

The Birthday Reminder System successfully demonstrates the practical application of Object-Oriented Programming principles, including encapsulation, abstraction, inheritance, and polymorphism.

The system achieves its goal of managing birthday data, providing reminders, and persisting information using a modular and extensible architecture. The use of design patterns, such as the Factory Pattern, improves flexibility and maintainability.

Overall, the coursework resulted in a functional, well-structured application that meets all defined requirements and provides a strong foundation for future enhancements such as real notification integration and graphical interfaces.

---

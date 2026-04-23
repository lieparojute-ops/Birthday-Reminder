
from datetime import date, datetime

class Birthday:
    def __init__(self, name, birth_date, note = ""):
        self.name = name
        self.birth_date = birth_date
        self.note = note

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value.strip():
            raise ValueError("Name cannot be empty.")
        self._name = value.strip()

    @property
    def birth_date(self):
        return self._birth_date

    @birth_date.setter
    def birth_date(self, value):
        try:
            self._birth_date = datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Birth date must be in YYYY-MM-DD format.")

    def days_until_birthday(self):
        today = date.today()
        next_birthday = self._birth_date.replace(year=today.year)

        if next_birthday < today:
            next_birthday = next_birthday.replace(year=today.year + 1)

        return (next_birthday - today).days
    
    def get_reminder_text(self):
        days = self.days_until_birthday()

        if days == 0:
            message = f"Today is {self.name}'s birthday"
        elif days == 1:
            message = f"{self.name}'s birthday is tomorrow"
        else:
            message = f"{self.name}'s birthday is in {days} days"

        if self.note:
            message += f" ({self.note})"

        return message

    def __str__(self):
        return f"Name: {self._name}, Birth date: {self._birth_date.strftime('%Y-%m-%d')}"

# test cases

birthday = Birthday("Alice", "2006-04-30")
print(birthday)
print(birthday.get_reminder_text())

birthday1 = Birthday("Bob", "1990-04-23", "Wish him a happy birthday!")
print(birthday1)
print(birthday1.get_reminder_text())

from datetime import datetime
import pickle
import copy


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, name):
        Field.__init__(self, name)
        self.name = name


class Phone(Field):
    def __init__(self, phone):
        Field.__init__(self, phone)
        phone_digits = ''.join(filter(str.isdigit, phone))
        if len(phone_digits) != 10:
            raise Exception("Invalid phone number")
        self.phone = phone


class Birthday:
    def __init__(self, birthday):
        self.birthday = birthday

    def __str__(self):
        return self.birthday.strftime('%d.%m.%Y')


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(None)

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def edit_phone(self, phone, new_phone):
        for i, p in enumerate(self.phones):
            if p.phone == phone:
                self.phones[i] = Phone(new_phone)
                return "Phone edited successfully."
        raise Exception("Missing phone number")

    def find_phone(self, phone):
        return phone in self.phones

    def add_birthday(self, birthday):
        date_format = "%d.%m.%Y"
        try:
            birthday_as_date = Birthday(
                datetime.strptime(birthday, date_format).date())
            self.birthday = birthday_as_date
        except ValueError:
            raise Exception("Please provide the date in the format DD.MM.YYYY")

    def __str__(self):
        return f"Contact name: {self.name.name}, phones: {'; '.join(str(p.phone) for p in self.phones)}"


class AddressBook():
    def __init__(self, filename: str):
        self.users = {}
        self.filename = filename

    def add_record(self, record):
        self.users[record.name.name] = record

    def find(self, name):
        if name in self.users:
            return self.users[name]
        raise Exception("Contact missing")

    def delete(self, name):
        self.users.pop(name)

    def __str__(self):
        all = str('\n')
        for record in self.users.values():
            all += str(record) + '\n'

        return all

    def get_birthdays_per_week(self):
        today = datetime.today().date()
        birthdays = {}
        for name, user in self.users.items():
            birthday = user.birthday
            birthday_this_year = birthday.replace(year=today.year)
            if birthday_this_year < today:
                birthday_this_year = birthday.replace(year=today.year + 1)
            if (birthday_this_year - today).days < 7:
                day_of_week = self.GetNameOfDay(birthday_this_year)
                if day_of_week in birthdays:
                    birthdays[day_of_week].append(name)
                else:
                    birthdays[day_of_week] = [name]
        result = ""
        for day, names in birthdays.items():
            result += f"{day} {', '.join(names)}\n"

        return result

    def GetNameOfDay(self, date):
        switcher = {
            0: "Monday",
            1: "Tuesday",
            2: "Wednesday",
            3: "Thursday",
            4: "Friday",
            5: "Saturday",
            6: "Sunday"
        }
        return switcher.get(date.weekday(), "Invalid day")

    def save_to_file(self):
        with open(self.filename, "wb") as file:
            pickle.dump(self, file)

    def read_from_file(self):
        with open(self.filename, "rb") as file:
            content = pickle.load(file)
        return content

from class_library import AddressBook, Record


def main():
    book = AddressBook("contacts")
    try:
        book = book.read_from_file()
        print("Contacts loaded")
    except Exception:
        print("Missing contacts")

    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        try:
            if command in ["close", "exit"]:
                print("Good bye!")
                break
            elif command == "hello":
                print("How can I help you?")
            elif command == "add":
                print(add_contact(args, book))
            elif command == "change":
                print(change_phone(args, book))
            elif command == "phone":
                print(get_phone(book, args))
            elif command == "all":
                print(book)
            elif command == "find":
                print(find_contact(book, args))
            elif command == "delete":
                print(delete_contact(book, args))
            elif command == "add-birthday":
                print(add_birthday(book, args))
            elif command == "show-birthday":
                print(show_birthday(book, args))
            elif command == "birthdays":
                print(birthdays(book))
            elif command == "save":
                print(save(book))
            else:
                print("Invalid command.")
        except Exception as e:

            print(f"{e}")


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def input_error(error_message):
    def decorator(func):
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except ValueError:
                return error_message

        return inner
    return decorator


@input_error("Give me name and phone please.")
def add_contact(args, adress_book):
    name, phone = args
    record = Record(name)
    record.add_phone(phone)
    adress_book.add_record(record)
    return "Contact added."


@input_error("Give me name and phone please.")
def change_phone(args, adress_book):
    name, phone, newPhone = args
    adress_book.find(name).edit_phone(phone, newPhone)
    return "Contact changed."


@input_error("Give me name please.")
def get_phone(adress_book, args):
    name, = args
    return f"Phones: {', '.join(str(p) for p in adress_book.find(name).phones)}"


@input_error("Give me name please.")
def find_contact(adress_book, args):
    name, = args
    return adress_book.find(name)


@input_error("Give me name please.")
def delete_contact(address_book, args):
    name, = args
    if address_book.find(name):
        address_book.delete(name)
        return "Contact deleted"
    return "Contact missing"


@input_error("Give me name and birthday please.")
def add_birthday(address_book, args):
    name, birthday = args
    address_book.find(name).add_birthday(birthday)
    return "Birthday added"


@input_error("Give me name please.")
def show_birthday(address_book, args):
    name, = args
    return str(address_book.find(name).birthday)


def birthdays(address_book):
    return address_book.get_birthdays_per_week()


def save(address_book):
    address_book.save_to_file()
    return "Contacts saved to file."


if __name__ == "__main__":
    main()

import csv
from connect import connect


def create_table():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(100) NOT NULL,
            phone VARCHAR(20) NOT NULL UNIQUE
        )
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("Table created successfully.")


def insert_from_csv(filename):
    conn = connect()
    cur = conn.cursor()

    with open(filename, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                cur.execute(
                    "INSERT INTO phonebook (first_name, phone) VALUES (%s, %s) ON CONFLICT (phone) DO NOTHING",
                    (row["first_name"], row["phone"])
                )
            except Exception as e:
                print("Error inserting row:", row, e)

    conn.commit()
    cur.close()
    conn.close()
    print("Data inserted from CSV.")


def insert_from_console():
    name = input("Enter name: ")
    phone = input("Enter phone: ")

    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO phonebook (first_name, phone) VALUES (%s, %s)",
            (name, phone)
        )
        conn.commit()
        print("Contact added.")
    except Exception as e:
        print("Error:", e)

    cur.close()
    conn.close()


def update_contact():
    name = input("Enter name to update: ")
    choice = input("1 - change name, 2 - change phone: ")

    conn = connect()
    cur = conn.cursor()

    if choice == "1":
        new_name = input("New name: ")
        cur.execute(
            "UPDATE phonebook SET first_name=%s WHERE first_name=%s",
            (new_name, name)
        )
    elif choice == "2":
        new_phone = input("New phone: ")
        cur.execute(
            "UPDATE phonebook SET phone=%s WHERE first_name=%s",
            (new_phone, name)
        )
    else:
        print("Wrong choice")
        cur.close()
        conn.close()
        return

    conn.commit()
    cur.close()
    conn.close()
    print("Updated.")


def show_all():
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM phonebook")
    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()


def search_by_name():
    name = input("Enter name: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM phonebook WHERE first_name ILIKE %s",
        ('%' + name + '%',)
    )

    rows = cur.fetchall()
    for row in rows:
        print(row)

    cur.close()
    conn.close()


def search_by_phone_prefix():
    prefix = input("Enter phone prefix: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM phonebook WHERE phone LIKE %s",
        (prefix + '%',)
    )

    rows = cur.fetchall()
    for row in rows:
        print(row)

    cur.close()
    conn.close()


def delete_by_name():
    name = input("Enter name to delete: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("DELETE FROM phonebook WHERE first_name=%s", (name,))
    conn.commit()

    cur.close()
    conn.close()
    print("Deleted.")


def delete_by_phone():
    phone = input("Enter phone to delete: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("DELETE FROM phonebook WHERE phone=%s", (phone,))
    conn.commit()

    cur.close()
    conn.close()
    print("Deleted.")


def menu():
    while True:
        print("\nPHONEBOOK MENU")
        print("1 - Create table")
        print("2 - Insert from CSV")
        print("3 - Insert manually")
        print("4 - Update contact")
        print("5 - Show all")
        print("6 - Search by name")
        print("7 - Search by phone prefix")
        print("8 - Delete by name")
        print("9 - Delete by phone")
        print("0 - Exit")

        choice = input("Choose: ")

        if choice == "1":
            create_table()
        elif choice == "2":
            insert_from_csv("contacts.csv")
        elif choice == "3":
            insert_from_console()
        elif choice == "4":
            update_contact()
        elif choice == "5":
            show_all()
        elif choice == "6":
            search_by_name()
        elif choice == "7":
            search_by_phone_prefix()
        elif choice == "8":
            delete_by_name()
        elif choice == "9":
            delete_by_phone()
        elif choice == "0":
            break
        else:
            print("Wrong choice")


if __name__ == "__main__":
    menu()
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

def search_by_pattern():
    pattern = input("Enter pattern: ")

    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute("SELECT * FROM search_phonebook(%s);", (pattern,))
        rows = cur.fetchall()

        for row in rows:
            print(row)
    except Exception as e:
        print("Error:", e)
    finally:
        cur.close()
        conn.close()

def insert_or_update_user():
    name = input("Enter name: ")
    phone = input("Enter phone: ")

    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute("CALL insert_or_update_user(%s, %s);", (name, phone))
        conn.commit()
        print("Done.")
    except Exception as e:
        conn.rollback()
        print("Error:", e)
    finally:
        cur.close()
        conn.close()

def insert_many_users():
    count = int(input("How many users? "))

    names = []
    phones = []

    for i in range(count):
        name = input(f"Enter name for user {i+1}: ")
        phone = input(f"Enter phone for user {i+1}: ")
        names.append(name)
        phones.append(phone)

    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute("CALL insert_many_users(%s, %s);", (names, phones))
        conn.commit()
        print("Done.")
    except Exception as e:
        conn.rollback()
        print("Error:", e)
    finally:
        cur.close()
        conn.close()

def show_paginated():
    limit_count = int(input("Enter LIMIT: "))
    offset_count = int(input("Enter OFFSET: "))

    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute(
            "SELECT * FROM get_phonebook_paginated(%s, %s);",
            (limit_count, offset_count)
        )
        rows = cur.fetchall()

        for row in rows:
            print(row)
    except Exception as e:
        print("Error:", e)
    finally:
        cur.close()
        conn.close()


def delete_user():
    value = input("Enter username or phone: ")

    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute("CALL delete_user(%s);", (value,))
        conn.commit()
        print("Deleted.")
    except Exception as e:
        conn.rollback()
        print("Error:", e)
    finally:
        cur.close()
        conn.close()


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
        print("10 - Search by pattern")
        print("11 - Insert or update user")
        print("12 - Insert many users")
        print("13 - Pagination")
        print("14 - Delete by username or phone")
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
        elif choice == "10":
            search_by_pattern()
        elif choice == "11":
            insert_or_update_user()
        elif choice == "12":
            insert_many_users()
        elif choice == "13":
            show_paginated()
        elif choice == "14":
            delete_user()
        elif choice == "0":
            break
        else:
            print("Wrong choice")


if __name__ == "__main__":
    menu()
import csv
import json
import os
from connect import connect


def run_sql_file(filename):
    if not os.path.exists(filename):
        print(f"{filename} not found.")
        return

    conn = connect()
    cur = conn.cursor()

    try:
        with open(filename, "r", encoding="utf-8") as file:
            sql = file.read()

        cur.execute(sql)
        conn.commit()
        print(filename, "executed successfully.")
    except Exception as e:
        conn.rollback()
        print("Error executing", filename, ":", e)
    finally:
        cur.close()
        conn.close()


def setup_database():
    run_sql_file("schema.sql")
    run_sql_file("functions.sql")
    run_sql_file("procedures.sql")


def create_table():
    # Old menu option kept from Practice 7.
    # Now it creates the full improved schema too.
    setup_database()


def get_group_id(cur, group_name):
    if group_name is None or group_name.strip() == "":
        group_name = "Other"

    cur.execute(
        "INSERT INTO groups (name) VALUES (%s) ON CONFLICT (name) DO NOTHING",
        (group_name,)
    )

    cur.execute("SELECT id FROM groups WHERE name=%s", (group_name,))
    return cur.fetchone()[0]


def add_or_update_contact(first_name, phone, email=None, birthday=None, group_name="Other", phone_type="mobile"):
    conn = connect()
    cur = conn.cursor()

    try:
        group_id = get_group_id(cur, group_name)

        if birthday == "":
            birthday = None

        cur.execute(
            """
            INSERT INTO phonebook (first_name, phone, email, birthday, group_id)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (phone)
            DO UPDATE SET
                first_name = EXCLUDED.first_name,
                email = EXCLUDED.email,
                birthday = EXCLUDED.birthday,
                group_id = EXCLUDED.group_id
            RETURNING id;
            """,
            (first_name, phone, email, birthday, group_id)
        )

        contact_id = cur.fetchone()[0]

        if phone_type not in ("home", "work", "mobile"):
            phone_type = "mobile"

        cur.execute(
            """
            INSERT INTO phones (contact_id, phone, type)
            VALUES (%s, %s, %s)
            ON CONFLICT (contact_id, phone) DO NOTHING;
            """,
            (contact_id, phone, phone_type)
        )

        conn.commit()
        print("Contact saved.")
    except Exception as e:
        conn.rollback()
        print("Error:", e)
    finally:
        cur.close()
        conn.close()


def insert_from_csv(filename):
    conn = connect()
    cur = conn.cursor()

    try:
        with open(filename, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                first_name = row.get("first_name", "").strip()
                phone = row.get("phone", "").strip()
                email = row.get("email", "").strip() or None
                birthday = row.get("birthday", "").strip() or None
                group_name = row.get("group", "Other").strip() or "Other"
                phone_type = row.get("type", "mobile").strip() or "mobile"

                if first_name == "" or phone == "":
                    print("Skipped invalid row:", row)
                    continue

                group_id = get_group_id(cur, group_name)

                cur.execute(
                    """
                    INSERT INTO phonebook (first_name, phone, email, birthday, group_id)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (phone)
                    DO UPDATE SET
                        first_name = EXCLUDED.first_name,
                        email = EXCLUDED.email,
                        birthday = EXCLUDED.birthday,
                        group_id = EXCLUDED.group_id
                    RETURNING id;
                    """,
                    (first_name, phone, email, birthday, group_id)
                )

                contact_id = cur.fetchone()[0]

                if phone_type not in ("home", "work", "mobile"):
                    phone_type = "mobile"

                cur.execute(
                    """
                    INSERT INTO phones (contact_id, phone, type)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (contact_id, phone) DO NOTHING;
                    """,
                    (contact_id, phone, phone_type)
                )

        conn.commit()
        print("Data inserted from CSV.")
    except Exception as e:
        conn.rollback()
        print("Error:", e)
    finally:
        cur.close()
        conn.close()


def insert_from_console():
    name = input("Enter name: ")
    phone = input("Enter main phone: ")
    email = input("Enter email (optional): ")
    birthday = input("Enter birthday YYYY-MM-DD (optional): ")
    group_name = input("Enter group Family/Work/Friend/Other: ")
    phone_type = input("Enter phone type home/work/mobile: ")

    add_or_update_contact(name, phone, email or None, birthday or None, group_name or "Other", phone_type or "mobile")


def update_contact():
    name = input("Enter name to update: ")

    print("1 - change name")
    print("2 - change main phone")
    print("3 - change email")
    print("4 - change birthday")
    print("5 - change group")
    choice = input("Choose: ")

    conn = connect()
    cur = conn.cursor()

    try:
        if choice == "1":
            new_name = input("New name: ")
            cur.execute("UPDATE phonebook SET first_name=%s WHERE first_name=%s", (new_name, name))

        elif choice == "2":
            new_phone = input("New phone: ")
            cur.execute("UPDATE phonebook SET phone=%s WHERE first_name=%s RETURNING id", (new_phone, name))
            row = cur.fetchone()

            if row:
                contact_id = row[0]
                cur.execute(
                    """
                    INSERT INTO phones (contact_id, phone, type)
                    VALUES (%s, %s, 'mobile')
                    ON CONFLICT (contact_id, phone) DO NOTHING
                    """,
                    (contact_id, new_phone)
                )

        elif choice == "3":
            new_email = input("New email: ")
            cur.execute("UPDATE phonebook SET email=%s WHERE first_name=%s", (new_email, name))

        elif choice == "4":
            new_birthday = input("New birthday YYYY-MM-DD: ")
            cur.execute("UPDATE phonebook SET birthday=%s WHERE first_name=%s", (new_birthday or None, name))

        elif choice == "5":
            group_name = input("New group: ")
            cur.execute("CALL move_to_group(%s, %s)", (name, group_name))

        else:
            print("Wrong choice")
            return

        conn.commit()
        print("Updated.")
    except Exception as e:
        conn.rollback()
        print("Error:", e)
    finally:
        cur.close()
        conn.close()


def print_contact_rows(rows):
    if len(rows) == 0:
        print("No contacts found.")
        return

    for row in rows:
        print(row)


def show_all():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            p.id,
            p.first_name,
            p.phone AS main_phone,
            p.email,
            p.birthday,
            COALESCE(g.name, 'No group') AS group_name,
            COALESCE(
                string_agg(ph.type || ':' || ph.phone, ', ' ORDER BY ph.id),
                ''
            ) AS all_phones,
            p.created_at
        FROM phonebook p
        LEFT JOIN groups g ON p.group_id = g.id
        LEFT JOIN phones ph ON ph.contact_id = p.id
        GROUP BY p.id, g.name
        ORDER BY p.id;
    """)

    rows = cur.fetchall()
    print_contact_rows(rows)

    cur.close()
    conn.close()


def search_by_name():
    name = input("Enter name: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT p.id, p.first_name, p.phone, p.email, p.birthday, g.name
        FROM phonebook p
        LEFT JOIN groups g ON p.group_id = g.id
        WHERE p.first_name ILIKE %s
        ORDER BY p.id
        """,
        ('%' + name + '%',)
    )

    print_contact_rows(cur.fetchall())

    cur.close()
    conn.close()


def search_by_phone_prefix():
    prefix = input("Enter phone prefix: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT DISTINCT p.id, p.first_name, p.phone, p.email, p.birthday, g.name
        FROM phonebook p
        LEFT JOIN groups g ON p.group_id = g.id
        LEFT JOIN phones ph ON ph.contact_id = p.id
        WHERE p.phone LIKE %s OR ph.phone LIKE %s
        ORDER BY p.id
        """,
        (prefix + '%', prefix + '%')
    )

    print_contact_rows(cur.fetchall())

    cur.close()
    conn.close()


def search_by_email():
    email = input("Enter email pattern: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT p.id, p.first_name, p.phone, p.email, p.birthday, g.name
        FROM phonebook p
        LEFT JOIN groups g ON p.group_id = g.id
        WHERE p.email ILIKE %s
        ORDER BY p.id
        """,
        ('%' + email + '%',)
    )

    print_contact_rows(cur.fetchall())

    cur.close()
    conn.close()


def filter_by_group():
    group_name = input("Enter group name: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT p.id, p.first_name, p.phone, p.email, p.birthday, g.name
        FROM phonebook p
        JOIN groups g ON p.group_id = g.id
        WHERE g.name ILIKE %s
        ORDER BY p.id
        """,
        (group_name,)
    )

    print_contact_rows(cur.fetchall())

    cur.close()
    conn.close()


def sort_contacts():
    print("1 - sort by name")
    print("2 - sort by birthday")
    print("3 - sort by date added")
    choice = input("Choose: ")

    if choice == "1":
        order_by = "p.first_name"
    elif choice == "2":
        order_by = "p.birthday NULLS LAST"
    elif choice == "3":
        order_by = "p.created_at"
    else:
        print("Wrong choice")
        return

    conn = connect()
    cur = conn.cursor()

    cur.execute(f"""
        SELECT p.id, p.first_name, p.phone, p.email, p.birthday, g.name, p.created_at
        FROM phonebook p
        LEFT JOIN groups g ON p.group_id = g.id
        ORDER BY {order_by};
    """)

    print_contact_rows(cur.fetchall())

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

    cur.execute(
        """
        DELETE FROM phonebook
        WHERE phone=%s
           OR id IN (SELECT contact_id FROM phones WHERE phone=%s)
        """,
        (phone, phone)
    )

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
        print_contact_rows(rows)
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
        name = input(f"Enter name for user {i + 1}: ")
        phone = input(f"Enter phone for user {i + 1}: ")
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
        print_contact_rows(cur.fetchall())
    except Exception as e:
        print("Error:", e)
    finally:
        cur.close()
        conn.close()


def paginated_navigation():
    limit_count = int(input("Page size: "))
    offset_count = 0

    while True:
        conn = connect()
        cur = conn.cursor()

        try:
            cur.execute(
                "SELECT * FROM get_phonebook_paginated(%s, %s);",
                (limit_count, offset_count)
            )
            rows = cur.fetchall()

            print("\nPAGE", offset_count // limit_count + 1)
            print_contact_rows(rows)
        except Exception as e:
            print("Error:", e)
        finally:
            cur.close()
            conn.close()

        command = input("next / prev / quit: ").lower()

        if command == "next":
            offset_count += limit_count
        elif command == "prev":
            offset_count = max(0, offset_count - limit_count)
        elif command == "quit":
            break
        else:
            print("Wrong command")


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


def add_phone_to_contact():
    name = input("Contact name: ")
    phone = input("New phone: ")
    phone_type = input("Type home/work/mobile: ")

    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute("CALL add_phone(%s, %s, %s);", (name, phone, phone_type))
        conn.commit()
        print("Phone added.")
    except Exception as e:
        conn.rollback()
        print("Error:", e)
    finally:
        cur.close()
        conn.close()


def move_contact_to_group():
    name = input("Contact name: ")
    group_name = input("New group name: ")

    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute("CALL move_to_group(%s, %s);", (name, group_name))
        conn.commit()
        print("Contact moved.")
    except Exception as e:
        conn.rollback()
        print("Error:", e)
    finally:
        cur.close()
        conn.close()


def export_to_json(filename="contacts_export.json"):
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            p.id,
            p.first_name,
            p.phone,
            p.email,
            p.birthday,
            COALESCE(g.name, 'Other') AS group_name
        FROM phonebook p
        LEFT JOIN groups g ON p.group_id = g.id
        ORDER BY p.id;
    """)

    contacts = []

    for contact_id, first_name, phone, email, birthday, group_name in cur.fetchall():
        cur.execute(
            "SELECT phone, type FROM phones WHERE contact_id=%s ORDER BY id",
            (contact_id,)
        )

        phones = []
        for phone_row, type_row in cur.fetchall():
            phones.append({
                "phone": phone_row,
                "type": type_row
            })

        contacts.append({
            "first_name": first_name,
            "phone": phone,
            "email": email,
            "birthday": str(birthday) if birthday else None,
            "group": group_name,
            "phones": phones
        })

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(contacts, file, indent=4, ensure_ascii=False)

    cur.close()
    conn.close()
    print("Exported to", filename)


def contact_exists(cur, first_name):
    cur.execute("SELECT id FROM phonebook WHERE first_name=%s ORDER BY id LIMIT 1", (first_name,))
    return cur.fetchone()


def delete_contact_by_name(cur, first_name):
    cur.execute("DELETE FROM phonebook WHERE first_name=%s", (first_name,))


def import_from_json(filename="contacts_export.json"):
    if not os.path.exists(filename):
        print(filename, "not found.")
        return

    with open(filename, "r", encoding="utf-8") as file:
        contacts = json.load(file)

    conn = connect()
    cur = conn.cursor()

    try:
        for item in contacts:
            first_name = item.get("first_name")
            phone = item.get("phone")
            email = item.get("email")
            birthday = item.get("birthday")
            group_name = item.get("group", "Other")
            phones = item.get("phones", [])

            if not first_name or not phone:
                print("Skipped invalid contact:", item)
                continue

            existing = contact_exists(cur, first_name)

            if existing:
                action = input(f"{first_name} already exists. skip / overwrite: ").lower()

                if action == "skip":
                    continue

                if action == "overwrite":
                    delete_contact_by_name(cur, first_name)
                else:
                    print("Wrong choice, skipped.")
                    continue

            group_id = get_group_id(cur, group_name)

            cur.execute(
                """
                INSERT INTO phonebook (first_name, phone, email, birthday, group_id)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id
                """,
                (first_name, phone, email, birthday, group_id)
            )

            contact_id = cur.fetchone()[0]

            if len(phones) == 0:
                phones = [{"phone": phone, "type": "mobile"}]

            for phone_item in phones:
                p = phone_item.get("phone")
                t = phone_item.get("type", "mobile")

                if t not in ("home", "work", "mobile"):
                    t = "mobile"

                if p:
                    cur.execute(
                        """
                        INSERT INTO phones (contact_id, phone, type)
                        VALUES (%s, %s, %s)
                        ON CONFLICT (contact_id, phone) DO NOTHING
                        """,
                        (contact_id, p, t)
                    )

        conn.commit()
        print("Import completed.")
    except Exception as e:
        conn.rollback()
        print("Error:", e)
    finally:
        cur.close()
        conn.close()


def menu():
    while True:
        print("\nPHONEBOOK MENU")
        print("1 - Create / update database schema")
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

        print("\nEXTENDED TASKS")
        print("15 - Add phone to existing contact")
        print("16 - Move contact to group")
        print("17 - Filter by group")
        print("18 - Search by email")
        print("19 - Sort contacts")
        print("20 - Pagination navigation")
        print("21 - Export contacts to JSON")
        print("22 - Import contacts from JSON")
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
        elif choice == "15":
            add_phone_to_contact()
        elif choice == "16":
            move_contact_to_group()
        elif choice == "17":
            filter_by_group()
        elif choice == "18":
            search_by_email()
        elif choice == "19":
            sort_contacts()
        elif choice == "20":
            paginated_navigation()
        elif choice == "21":
            export_to_json()
        elif choice == "22":
            import_from_json()
        elif choice == "0":
            break
        else:
            print("Wrong choice")


if __name__ == "__main__":
    menu()
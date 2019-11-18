import argparse
import mysql.connector


records = ["id", "name", "surname", "address", "phone number", "email address"]


def parse():
    parser = argparse.ArgumentParser(description="Manage contact info")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-a", "--add", help="Add contact", action="store_true")
    group.add_argument("-d", "--delete", help="Delete contact", action="store_true")
    group.add_argument("-u", "--update", help="Update contact", action="store_true")
    group.add_argument("-l", "--list", help="List contacts", action="store_true")
    parser.add_argument("-p", "--alpha", help="Display alphabetical list")
    parser.add_argument("-c", "--creation", help="Display content creation date")
    return parser.parse_args()


def select(cursor):
    name, surname = input("Input name and surname to delete:").split()
    sel_query = 'SELECT * FROM contacts WHERE name like %s AND surname like %s'
    cursor.execute(sel_query, (name, surname))
    result = cursor.fetchall()
    return result[0][0]


def delete(cursor, delete_id):
    delete_query = 'DELETE from contacts WHERE id = %s'
    cursor.execute(delete_query, (delete_id,))


def update(cursor, update_id):
    print("Left blank if not changed")
    while True:
        input_dict = {"name": input("Name: "), "surname": input("Surname: "), "address": input("Address: "),
                  "number": input("Phone number:"), "email": input("Email address: ")}
        try:
            int(input_dict[number])
            break
        except ValueError:
            print("Phone number should be a number")
    for i in input_dict:
        if input_dict[i] != "":
            update_query = 'UPDATE contacts SET {} = %s where id = %s'.format(i)
            cursor.execute(update_query, (input_dict[i], update_id))


def add(cursor):
    add_query = "INSERT INTO contacts (name, surname, address, number, email) VALUES (%s, %s, %s, %s, %s)"
    while True:
        val = (input("Name: "), input("Surname: "), input("Address: "), input("Phone number:"),
               input("Email address: "))
        try:
            int(val[3])
            break
        except ValueError:
            print("Phone number should be a number!")
    cursor.execute(add_query, val)


def main():
    args = parse()
    contacts = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        passwd="password",
        database="contacts"
    )

    cursor = contacts.cursor()

    if args.add:
        add(cursor)
        contacts.commit()
    if args.delete:
        delete_id = select(cursor)
        delete(cursor, delete_id)
        contacts.commit()
    if args.update:
        update_id = select(cursor)
        update(cursor, update_id)
        contacts.commit()
    if args.list:
        cursor.execute("SELECT * FROM contacts")
        result = cursor.fetchall()
        for record in records:
            print(record.ljust(18), end=" ")
        print("")
        for row in result:
            for x in row:
                # s = str(x)
                print(str(x).ljust(18), end=" ")
            print("")


if __name__ == "__main__":
    main()

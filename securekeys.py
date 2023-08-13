import sqlite3

# Basic Caesar cipher encryption
def encrypt_password(password, key):
    encrypted = ""
    for char in password:
        encrypted_char = chr((ord(char) + key) % 128)
        encrypted += encrypted_char
    return encrypted

# Basic Caesar cipher decryption
def decrypt_password(encrypted_password, key):
    decrypted = ""
    for char in encrypted_password:
        decrypted_char = chr((ord(char) - key) % 128)
        decrypted += decrypted_char
    return decrypted

# Initialize the database connection
def initialize_database():
    conn = sqlite3.connect('passwords.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS passwords (website TEXT, username TEXT, encrypted_password TEXT)')
    conn.commit()
    return conn, cursor

# Add a new password entry
def add_password(conn, cursor, website, username, encrypted_password):
    cursor.execute('INSERT INTO passwords VALUES (?, ?, ?)', (website, username, encrypted_password))
    conn.commit()

# Retrieve passwords for a specific website
def get_passwords_for_website(cursor, website):
    cursor.execute('SELECT username, encrypted_password FROM passwords WHERE website = ?', (website,))
    return cursor.fetchall()

if __name__ == "__main__":
    conn, cursor = initialize_database()

    while True:
        print("1. Store Password")
        print("2. Retrieve Passwords")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            website = input("Enter website: ")
            username = input("Enter username: ")
            password = input("Enter password: ")

            key = int(input("Enter encryption key: "))
            encrypted_password = encrypt_password(password, key)
            add_password(conn, cursor, website, username, encrypted_password)
            print("Password stored successfully!")

        elif choice == '2':
            website = input("Enter website to retrieve passwords for: ")
            passwords = get_passwords_for_website(cursor, website)

            if passwords:
                for username, encrypted_password in passwords:
                    key = int(input("Enter decryption key: "))
                    decrypted_password = decrypt_password(encrypted_password, key)
                    print(f"Website: {website}, Username: {username}, Password: {decrypted_password}")
            else:
                print("No passwords found for the given website.")

        elif choice == '3':
            conn.close()
            break

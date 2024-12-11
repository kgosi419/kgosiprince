import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('ebookstore.db')
cursor = conn.cursor()

# Create the books table
cursor.execute('''
CREATE TABLE IF NOT EXISTS book (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    qty INTEGER NOT NULL
)
''')

# Insert initial book data
book = [
    (3001, "A Tale of Two Cities", "Charles Dickens", 30),
    (3002, "Harry Potter and the Philosopher's Stone", "J.K. Rowling", 40),
    (3003, "The Lion, the Witch and the Wardrobe", "C. S. Lewis", 25),
    (3004, "The Lord of the Rings", "J.R.R. Tolkien", 37),
    (3005, "Alice in Wonderland", "Lewis Carroll", 12),
    (3006, "If I Can, You Can", "Sally Eichhorst", 12),
    (3007, "The Great Gatsby", "F. Scott Fitzgerald", 15)
]

# Insert books, ignore duplicates
cursor.executemany(
    'INSERT OR IGNORE INTO book (id, title, author, qty) VALUES (?, ?, ?, ?)',
    book
)
conn.commit()


# Function to display the menu
def display_menu():
    print("\nBookstore Management System")
    print("1. Enter book")
    print("2. Update book")
    print("3. Delete book")
    print("4. Search books")
    print("0. Exit")


# Function to add a new book
def add_book():
    id = int(input("Enter book ID: "))
    title = input("Enter book title: ")
    author = input("Enter book author: ")
    qty = int(input("Enter quantity: "))

    cursor.execute(
        'INSERT INTO book (id, title, author, qty) VALUES (?, ?, ?, ?)',
        (id, title, author, qty)
    )
    conn.commit()
    print("Book added successfully.")


# Function to update an existing book
def update_book():
    id = int(input("Enter book ID to update: "))
    new_title = input("Enter new title: ")
    new_author = input("Enter new author: ")
    new_qty = int(input("Enter new quantity: "))

    cursor.execute(
        'UPDATE book SET title = ?, author = ?, qty = ? WHERE id = ?',
        (new_title, new_author, new_qty, id)
    )
    conn.commit()

    if cursor.rowcount == 0:
        print("Book not found.")
    else:
        print("Book updated successfully.")


# Function to delete a book
def delete_book():
    id = int(input("Enter book ID to delete: "))
    cursor.execute('DELETE FROM book WHERE id = ?', (id,))
    conn.commit()

    if cursor.rowcount == 0:
        print("Book not found.")
    else:
        print("Book deleted successfully.")


# Function to search for books
def book():
    query = input("Enter a keyword to search (title or author): ")
    cursor.execute(
        'SELECT * FROM book WHERE title LIKE ? OR author LIKE ?',
        ('%' + query + '%', '%' + query + '%')
    )
    results = cursor.fetchall()

    if results:
        print("\nSearch Results:")
        for row in results:
            print(f"ID: {row[0]}, Title: {row[1]}, Author: {row[2]}, Quantity: {row[3]}")
    else:
        print("No books found.")


# Main function to run the program
def main():
    while True:
        display_menu()
        choice = input("Select an option: ")

        if choice == '1':
            add_book()
        elif choice == '2':
            update_book()
        elif choice == '3':
            delete_book()
        elif choice == '4':
            book()
        elif choice == '0':
            print("Exiting the program.")
            break
        else:
            print("Invalid selection. Please try again.")


if __name__ == "__main__":
    main()

# Close the database connection
cursor.close()
conn.close()

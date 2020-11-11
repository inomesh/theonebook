import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():

    # List all Books.
    Books = db.execute("SELECT id, title, author, year FROM Books").fetchall()
    for Book in Books:
        print(f"Book {Book.id}: {Book.title} written by {Book.author}, {Book.year}")

    # Prompt user to choose a Book.
    Book_id = int(input("\nBook ID: "))
    Book = db.execute("SELECT title, author, year FROM Books WHERE id = :id",
                        {"id": Book_id}).fetchone()

    # Make sure Book is valid.
    if Book is None:
        print("Error: No such Book.")
        return

    # List readers.
    readers = db.execute("SELECT name FROM readers WHERE Book_id = :Book_id",
                            {"Book_id": Book_id}).fetchall()
    print("\nreaders:")
    for reader in readers:
        print(reader.name)
    if len(readers) == 0:
        print("No readers.")

if __name__ == "__main__":
    main()

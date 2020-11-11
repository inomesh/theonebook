import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():
    f = open("Readers.csv")
    rreader = csv.reader(f)
    for first_name, last_name, email, password, Book_id in rreader:
        db.execute("INSERT INTO readers (first_name, last_name, email, password, Book_id) VALUES(:first_name, :last_name, :email, :password, :Book_id)",
         { "first_name": first_name, "last_name": last_name, "email": email , "password": password, "Book_id": Book_id} )
        
        print(f"Added Book")
    db.commit()

if __name__ == "__main__":
    main()

  
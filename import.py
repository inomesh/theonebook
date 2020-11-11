import csv
import os
import re

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

#def main():
#    f = open("books1.csv")
#    rreader = csv.reader(f)
#    for isbn, title, author, year in rreader:
#        db.execute("INSERT INTO Books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
#                    {"isbn": isbn, "title": title, "author": author, "year": year})
#        print(f"Added Book from {title} .")
#    db.commit()
#
#if __name__ == "__main__":
#    main()

def main():
 
     data = []
     query = 'hello how are you'
    # data = db.execute("SELECT * FROM readers WHERE email= :email and password= :password ",
     #         {"email":email, "password":password}).fetchone()
     query = query.split(" ")
     for q in query:
         data.append(q)
     print("data is ",data)
    

if __name__ == "__main__":
    main()


'''@app.route("/signin", methods=["POST", "GET"])
@app.route("/Signin.html", methods=["POST", "GET"])
@app.route("/templates/Signin.html", methods=["POST", "GET"])
def login():
    session.pop('email', None)
    session.pop('password', None)
    if request.method == "POST":
       # Books = db.execute("SELECT * FROM readers").fetchall()
       #check if email even exist or not.
       session.permanent = True 

       
       email = str(request.form.get("Semail"))
       password = str(request.form.get("Spassword"))
       data = db.execute("SELECT * FROM readers WHERE email= :email and password= :password ",
              {"email":email, "password":password}).fetchone()
       try:
         if email == data["email"] and password == data["password"]:
            session["email"] = email
            session["password"] = password
            return render_template("mysession.html")
         else: 
            return render_template("error.html", message="Please register before signing in!") 
       except TypeError:
            return render_template("error.html")
               
    elif request.method == "GET":  
            if 'email' and 'password' in session:
             return redirect(url_for('mysession'))

    return render_template("Signin.html")
'''   
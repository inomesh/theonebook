import os
import requests
import json
import re
from flask import Flask, render_template, request, redirect, session, url_for, make_response
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from datetime import timedelta
from RegEx import emailCheck, pas

app = Flask(__name__)
app.secret_key = '-j9bm3cjSXfnWPRWCB1m4A'
app.config["SESSION_TYPE"]="filesystem"
app.permanent_session_lifetime = timedelta(minutes=30)
Session(app)
# engine = create_engine(os.getenv("DATABASE_URL"))
engine = create_engine('postgres://tmlxcfrvsatjgg:d215bdddac586972bd2e4f6885610673b6668980f996ea118ba3b0c943d90c4d@ec2-34-232-147-86.compute-1.amazonaws.com:5432/d4d2jgfg4do9a2')
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
@app.route("/index.html", methods=["POST", "GET"])
def index():
    #users registration check & storage
   # return render_template("index.html", Books=Books) || Books = db.execute("SELECT * FROM readers").fetchall()
    if request.method == "GET":
        return render_template("index.html")
      
    if  request.method == "POST":
      
     fname = str(request.form.get("fname"))
     lname = str(request.form.get("lname"))
    #email pattern matching verification
     email = str(request.form.get("email"))
     password = request.form.get("password")
     data = db.execute("SELECT * FROM readers WHERE first_name= :fname and last_name= :lname and email = :email ",
            {"fname":fname, "lname":lname ,"email":email}).fetchall()
     try:
         if len(data) != 0:
             print(fname, lname, len(data))
             return  render_template("error.html", message= "email already exist, please try to log in.") 
                    

         else: 
             if len(data) == 0:
                print(fname, lname)
                db.execute("INSERT INTO readers (first_name, last_name, email, password) VALUES (:fname, :lname, :email, :password)",
                {"fname": fname, "lname": lname, "email": email, "password": password })
                db.session.commit()
                return redirect(url_for("login"))   
            
     except ValueError: 
         return render_template("error.html")
     
         
 #login/authentication system is here.

@app.route("/signin", methods=["POST", "GET"])
@app.route("/Signin.html", methods=["POST", "GET"])
@app.route("/templates/Signin.html", methods=["POST", "GET"])
def login():
    session.pop('email', None)
    session.pop('password', None)
    if request.method == "POST":
       # Books = db.execute("SELECT * FROM readers").fetchall()
       #check if email even exist or not.
       session.permanent = True 
       session["email"] = str(request.form.get("Semail"))
       session["password"] = str(request.form.get("Spassword"))
       data = db.execute("SELECT * FROM readers WHERE email= :email and password= :password ",
              {"email":session["email"], "password":session["password"]}).fetchone()
       print(data)
       try:
            if len(data) != 0:
             return redirect(url_for('mysession'))
            else:
             return render_template("error.html") 
       except TypeError:
            return render_template("error.html")
               
    elif request.method == "GET":  
            if 'email' and 'password' in session:
             return redirect(url_for('mysession'))

    return render_template("Signin.html")
    


# user session is here and can be accessed only after authentication.

@app.route("/mysession", methods=["POST","GET"])
def mysession():

    if request.method == "GET":
        if "email" and "password" in session:
            print(session.get('email'))
            print("cool")
            user = db.execute("SELECT * FROM readers WHERE email= :email and password= :password ",
             {"email":session["email"], "password":session["password"]}).fetchone()
            print(user)
            Books = db.execute("SELECT * FROM Books").fetchall()
            return render_template("mysession.html", Books=Books)
        else:
            return render_template("error.html", message="not alowed, please try to log in first.")
    
  # ( if request.mmethod == "POST":
  #      newisbn = str(request.form.get("newISBN"))
  #      user = db.execute("SELECT * FROM Books WHERE isbn= :isbn",{"isbn":newisbn}).fetchone()
  #      return render_template("mysession.html")
        
   
@app.route("/update", methods=["POST", "GET"])
def update():
    if request.method == "POST":
        update_data = str(request.form['newISBN'])
        user_email = session.get('email')
        book = db.execute("SELECT * FROM Books WHERE isbn = :bisbn", {"bisbn": update_data }).fetchone()
        if update_data == book["isbn"]:
            addbook =   db.execute("UPDATE readers SET book_id = :bookid WHERE email = :useremail", { 
                        "bookid": book["id"] ,"useremail": user_email })
            db.commit()
        return render_template("mysession.html", addbook = addbook)
    else:
        return "404"





@app.route("/signout", methods=["POST", "GET"])
def signout():
        session.pop('email', None)
        session.pop('password', None)
        return redirect(url_for('login'))








@app.route("/api/<string:isbn>", methods=["GET"])
def Booksthrapi(isbn):
 #   """fetching the Book details from goodreads.com through api."""

    #make sure Books exist in our database && if not then it should return error 404!
    mybookdb = db.execute("SELECT * FROM Books WHERE isbn = :isbn  ", {"isbn": isbn}).fetchone()
    mybookapi = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "JYC9HrPZ5O6ADR5ZlZCzw", "isbns": isbn })
    try:
        mybookapi = mybookapi.json()
        for book in mybookapi['books']:
            reviews = book['reviews_count']
            ratings = book['average_rating']
            
        return render_template("dbBooks.html",mybookdb=mybookdb, reviews=reviews, ratings=ratings)
    except json.decoder.JSONDecodeError:
        return render_template("error.html", message= "Sorry! ")







@app.route("/books", methods=["GET","POST"])
def books():
    """Lists all Books."""
    Books = db.execute("SELECT * FROM Books").fetchall()
    return render_template("WebBooks.html", Books=Books)






@app.route("/books/<int:Book_id>")
def Book(Book_id):
    """Lists details about a single Book."""

    # Make sure flight exists.
    Book = db.execute("SELECT * FROM Books WHERE id = :id", {"id": Book_id}).fetchone()
    if Book is None:
        return render_template("error.html", message="No such Book is uploaded yet.")

    # Get all passengers.
    reads = db.execute("SELECT first_name FROM readers WHERE Book_id = :Book_id",
                            {"Book_id": Book_id}).fetchall()
    return render_template("Books.html", Book=Book, reads=reads)






@app.route("/search", methods=["GET", "POST"]) 
def search():
    quesryset = []
    text = str(request.form.get("search"))
    print(text)
    if text is None:
        print("none")
    if not text is None:
     query = text.split()
     for q in query:
        quesryset.append(q)
     print("cool")
     print(quesryset)
    return render_template("search.html")



#cookies

@app.route("/Signin/cookies", methods=["POST", "GET"])
def cookies():

    res = make_response("cookies", 200)
    res.set_cookie("TheOneBook", 
                    value = "Books",
                    max_age = 10,
                    expires = timedelta(minutes=10),
                    path = request.path,
                    domain = None,
                    secure = False,
                    httponly = False,
                    samesite = False
                    )
    

    return res




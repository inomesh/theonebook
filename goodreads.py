import os
import requests
import csv
from xml.etree import ElementTree
import json

#with open('newisbn.csv','r') as csv_file:
 #   csv_reader = csv.reader(csv_file)
  #  for line in csv_reader:
   #     print(line)
        
#res = requests.get("https://www.goodreads.com/book/isbn_to_id", params={"key": "JYC9HrPZ5O6ADR5ZlZCzw", "isbns": 9780553803709})
#print(res)
#for book in books['books']:
 #   print(book)

books = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "JYC9HrPZ5O6ADR5ZlZCzw", "isbns": 553804812})
try:
   books = books.json()
   for book in books['books']:
      reviews = book['reviews_count']
      ratings = book['average_rating']
   print(reviews)
   print(ratings)
except json.decoder.JSONDecodeError:
   print("error")

   




   
 



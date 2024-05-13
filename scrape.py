import requests
from bs4 import BeautifulSoup
import sqlite3
import csv
import sys

with open("sites.txt", "r") as f:
    site_names = [line.strip() for line in f.readlines()]

with open("authors.txt", "r") as f:
    author_names = [line.strip() for line in f.readlines()]

print("choose an option:")
print("1. store articles in sqlite database")
print("2. store articles in csv file")
option = input("(1/2): ")

if option != 1 or option != 2:
    print("invalid option. exiting.")
    sys.exit()

print("choose a site:")
for i, site in enumerate(site_names):
    print(f"{i+1}. {site}")
site_choice = int(input("enter your choice: "))
base_url = site_names[site_choice-1]

print("choose an author:")
for i, author in enumerate(author_names):
    print(f"{i+1}. {author}")
author_choice = int(input("enter your choice: "))
author_name = author_names[author_choice-1]

response = requests.get(base_url)

soup = BeautifulSoup(response.content, "html.parser")

articles = soup.find_all("article")

if option == "1":
    conn = sqlite3.connect("author_articles.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            title TEXT,
            url TEXT,
            author TEXT
        )
    """)

    for article in articles:
        author = article.find("span", {"class": "author"}).text.strip()
        
        if author == author_name:
            title = article.find("h2", {"class": "title"}).text.strip()
            url = article.find("a", {"class": "read-more"})["href"]
            
            cursor.execute("INSERT INTO articles (title, url, author) VALUES (?,?,?)",
                           (title, url, author))

    conn.commit()
    conn.close()

elif option == "2":
    with open("author_articles.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        
        writer.writerow(["title", "url", "author"])
        
        for article in articles:
            author = article.find("span", {"class": "author"}).text.strip()
            
            if author == author_name:
                title = article.find("h2", {"class": "title"}).text.strip()
                url = article.find("a", {"class": "read-more"})["href"]
                quote = '"'

                writer.writerow([quote+title+quote, quote+url+quote, quote+author+quote])
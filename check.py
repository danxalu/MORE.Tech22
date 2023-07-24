import requests
import urllib.request
import json

def showNews(url):
    with urllib.request.urlopen(url) as url_:
        data = json.load(url_)
        print(data)

url = "http://127.0.0.1:5000/news/accountant"
print("Accountant:")
showNews(url)

url = "http://127.0.0.1:5000/news/director"
print("Director:")
showNews(url)

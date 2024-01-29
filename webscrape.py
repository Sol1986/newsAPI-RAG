from dotenv import load_dotenv
from bs4 import BeautifulSoup
import json
import os
import requests
import re

load_dotenv()

api_key = os.getenv('API_KEY')

#API endpoint for fetching top headlines
api_url = 'https://newsapi.org/v2/top-headlines?country=us&category=business&apiKey='+api_key

#function to scrape content from a URL
def scrape_url(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup.get_text()
    except Exception as e:
        return str(e)

#fetch metadata from the API
response = requests.get(api_url)
data = response.json()

#list to hold data
articles = []

#loop through each headline, scrape content, and add to the list

for headline in data['articles']:
    headline_url = headline['url'] # Use the URL from the headline data
    content = scrape_url(headline_url)
    articles.append({
        'url': headline_url,
        'title': headline['title'],
        'content': content
        })

#save the data to a JSON file 
with open('articles.json', 'w', encoding='utf-8') as f:
    json.dump(articles, f, ensure_ascii=False, indent =4)




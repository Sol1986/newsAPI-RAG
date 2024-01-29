import requests
from dotenv import load_dotenv
import os
from newsapi import NewsApiClient
load_dotenv()


api_key = 'API_KEY'
base_url = 'https://newsapi.org/v2/top-headlines'

params = {
    'apiKey': os.getenv(api_key),
    'country': 'us'  # Example parameter: get top headlines from the US
}

response = requests.get(base_url, params=params)


if response.status_code == 200:
    news_data = response.json()
    articles = news_data['articles']
    for article in articles:
        print(article['title'])
else:
    print('Failed to retrieve news')


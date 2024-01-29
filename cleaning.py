import re
import json

def clean_text(text):
    # Remove HTML tags
    text = re.sub('<.*?>', '', text)
    # Replace newline characters and multiple spaces with a single space
    text = re.sub('\s+', ' ', text).strip()
    return text


with open('articles.json', 'r', encoding='utf-8') as file:
    articles = json.load(file)

for article in articles:
    article['content'] = clean_text(article['content'])

with open('cleaned_articles.json', 'w', encoding='utf-8') as file:
    json.dump(articles, file, ensure_ascii=False, indent=4)
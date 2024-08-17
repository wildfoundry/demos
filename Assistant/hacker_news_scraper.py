import requests
from bs4 import BeautifulSoup
from datetime import datetime

def fetch_hacker_news():
    url = 'https://news.ycombinator.com/'
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to load page {url}")

    soup = BeautifulSoup(response.text, 'html.parser')
    articles = []

    items = soup.select('tr.athing')
    for item in items:
        title_element = item.select_one('.titleline > a')
        if title_element:
            title = title_element.text
            link = title_element['href']
            if link.startswith('item?id='):
                link = 'https://news.ycombinator.com/' + link
            subtext = item.find_next_sibling('tr')
            date = subtext.select_one('.age')['title'] if subtext and subtext.select_one('.age') else 'N/A'
            
            articles.append({
                'title': title,
                'link': link,
                'date': date
            })

    return articles

from hacker_news_scraper import fetch_hacker_news


def main():
    articles = fetch_hacker_news()
    for article in articles:
        print(f"Title: {article['title']}")
        print(f"Link: {article['link']}")
        print(f"Date: {article['date']}")
        print('---')

if __name__ == "__main__":
    main()
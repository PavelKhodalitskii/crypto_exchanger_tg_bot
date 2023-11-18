import requests
from bs4 import BeautifulSoup
import datetime


def get_news():
    headers = {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                            " Chrome/119.0.0.0 Safari/537.36"
            }
    count_pages = 2
    for URL in [("https://bits.media/news/?nav_feed=page-" + str(i)) for i in range(1, count_pages + 1)]:
        page = requests.get(url=URL, headers=headers)
        soup = BeautifulSoup(page.content, "html.parser")
        news = soup.find_all("div", class_="news-item")
        for new in news:
            date = datetime.datetime.now()
            #current_date дате сегодня, можно поменять на другую дату
            current_date = str(date.day) + '.' + str(date.month) + '.' + str(date.year)
            if (new.find("span", class_="news-date").text.strip()) == current_date:
                news_date = new.find("span", class_="news-date").text.strip()
                news_name = new.find("a", class_="news-name").text.strip()
                news_text = new.find("div", class_="news-text").text.strip()
                url = f'https://bits.media{new.find("a", class_="news-name", href=True)["href"].strip()}'
                news_data = {
                    "news_date": news_date,
                    "news_name": news_name,
                    "news_text": news_text,
                    "url": url
                }
            else:
                break
    return news_data
import sys
from bs4 import BeautifulSoup as BS
from typing import Optional, List, TypedDict
import requests
import time
from tech_news.database import create_news


sys.setrecursionlimit(100000)


class NewsInfo(TypedDict):
    url: str
    title: str
    timestamp: str
    writer: str
    reading_time: int
    summary: str
    category: str


# Requisito 1 initial commit
def fetch(url: str) -> Optional[str]:
    HEADERS = {"user-agent": "Fake user-agent"}
    try:
        response = requests.get(url, headers=HEADERS, timeout=3)
        response.raise_for_status()
    except (requests.ReadTimeout, requests.HTTPError):
        return None
    else:
        return response.text
    finally:
        time.sleep(1)


# Requisito 2
def scrape_updates(html_content: str) -> List[str]:
    soup = BS(html_content, "lxml")
    articles = soup.find_all("article", class_="entry-preview")
    links = []
    for article in articles:
        article_link = article.find("h2", class_="entry-title").a["href"]
        links.append(article_link)
    return links


# Requisito 3
def scrape_next_page_link(html_content: str) -> Optional[str]:
    soup = BS(html_content, "lxml")
    try:
        return soup.find("a", class_="next")["href"]
    except TypeError:
        return None


# Requisito 4
def scrape_news(html_content: str) -> NewsInfo:
    soup = BS(html_content, "lxml")
    page_url = soup.head.find("link", attrs={"rel": "canonical"})["href"]
    page_title = soup.h1.string.strip()
    author = soup.find("span", class_="author").a.string
    summary = soup.find("div", class_="entry-content").p.get_text().strip()
    reading_time = (
        soup.find("li", class_="meta-reading-time").get_text().split(" ")[0]
    )
    date = soup.find("li", class_="meta-date").string
    category = (
        soup.find("div", class_="meta-category")
        .find("span", class_="label")
        .string
    )
    return {
        "url": page_url,
        "title": page_title,
        "writer": author,
        "summary": summary,
        "reading_time": int(reading_time),
        "timestamp": date,
        "category": category,
    }


# Requisito 5
def get_tech_news(amount: int) -> Optional[List[NewsInfo]]:
    all_news_by_page: List[NewsInfo] = []
    all_news: List[NewsInfo] = []
    ARTICLES_PER_PAGE = 12
    number_of_pages = get_number_of_pages(amount, ARTICLES_PER_PAGE)
    page_number = 1
    iteration = 0
    page_url = "https://blog.betrybe.com"
    while True and page_number <= number_of_pages:
        html_page_text = fetch(page_url)
        if not html_page_text:
            return None
        url_list = scrape_updates(html_page_text)
        url_list_length = len(url_list)
        if url_list_length == 0:
            return None
        iteration = iterate_all_news(
            all_news_by_page, url_list, amount, iteration
        )
        update_news_list(all_news_by_page, all_news)
        page_url = scrape_next_page_link(html_page_text)
        page_number += 1
        if not page_url:
            break
    create_news(all_news)
    return all_news


def update_news_list(
    all_news_by_page: List[NewsInfo], all_news: List[NewsInfo]
):
    all_news.extend(all_news_by_page)
    all_news_by_page.clear()


def iterate_all_news(
    all_news_by_page: List[NewsInfo],
    url_list: List[str],
    amount: int,
    iteration: int,
) -> int:
    for link in url_list:
        if iteration == amount:
            break
        news_html_text = fetch(link)
        if not news_html_text:
            continue
        news_info_dict = scrape_news(news_html_text)
        all_news_by_page.append(news_info_dict)
        iteration += 1
    return iteration


def get_number_of_pages(amount: int, items_per_page: int) -> int:
    return ((amount - 1) // items_per_page) + 1

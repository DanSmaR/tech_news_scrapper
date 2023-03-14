from bs4 import BeautifulSoup as BS
import requests
import time


# Requisito 1 initial commit
def fetch(url):
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
def scrape_updates(html_content):
    soup = BS(html_content, "lxml")
    articles = soup.find_all("article", class_="entry-preview")
    links = []
    for article in articles:
        article_link = article.find("h2", class_="entry-title").a["href"]
        links.append(article_link)
    return links


# Requisito 3
def scrape_next_page_link(html_content):
    soup = BS(html_content, "lxml")
    try:
        return soup.find("a", class_="next")["href"]
    except TypeError:
        return None


# Requisito 4
def scrape_news(html_content):
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
def get_tech_news(amount):
    """Seu código deve vir aqui"""

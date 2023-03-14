from bs4 import BeautifulSoup
import requests
import time


# Requisito 1 initial commit
def fetch(url: str):
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
    """Seu código deve vir aqui"""


# Requisito 3
def scrape_next_page_link(html_content):
    """Seu código deve vir aqui"""


# Requisito 4
def scrape_news(html_content):
    """Seu código deve vir aqui"""


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""

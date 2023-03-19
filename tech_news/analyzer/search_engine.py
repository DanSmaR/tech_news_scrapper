from datetime import datetime
from tech_news.database import db


# Requisito 7
def search_by_title(title):
    query = {"title": {"$regex": title, "$options": "i"}}
    fields = {"_id": 0, "title": 1, "url": 1}
    result = db.news.find(query, fields)
    tupled_list = [(news["title"], news["url"]) for news in list(result)]
    return tupled_list


# Requisito 8
def search_by_date(date):
    try:
        date = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Data inválida")
    else:
        formatted_date = date.strftime("%d/%m/%Y")
        result = db.news.find(
            {"timestamp": formatted_date}, {"_id": 0, "title": 1, "url": 1}
        )
        tupled_list = [(news["title"], news["url"]) for news in list(result)]
    return tupled_list


# Requisito 9
def search_by_category(category):
    """Seu código deve vir aqui"""

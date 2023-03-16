from tech_news.database import db


# Requisito 7
def search_by_title(title):
    query = {"title": {"$regex": title, "$options": "i"}}
    fields = {"_id": 0, "title": 1, "url": 1}
    result = db.news.find(query, fields)
    tupled_list = [
        (news["title"], news["url"]) for news in list(result)
    ]
    return tupled_list


# Requisito 8
def search_by_date(date):
    """Seu código deve vir aqui"""


# Requisito 9
def search_by_category(category):
    """Seu código deve vir aqui"""

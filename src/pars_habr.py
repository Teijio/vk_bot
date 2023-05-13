import requests
from rss_parser import Parser
from dataclasses import dataclass

import exceptions

URL = "https://habr.com/ru/rss/best/daily/?fl=ru"


@dataclass
class ItemData:
    title: str
    data: str


def extract_data(text: str) -> str:
    idx = text.find(" Читать дал")
    return text[:idx].strip()


def rss_parse_feed():
    xml = requests.get(URL)
    try:
        parser = Parser(xml=xml.content, limit=1)
        feed = parser.parse()
    except exceptions.ParseStatusException:
        raise

    item = feed.feed[0]
    data = extract_data(item.description)
    item_data = ItemData(title=item.title, data=data)

    return item_data

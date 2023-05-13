import requests
from rss_parser import Parser
from typing import Tuple


def extract_data(text: str) -> str:
    idx = text.find(" Читать дал")
    return text[:idx].strip()


def rss_parse_feed() -> Tuple[str, str]:
    xml = requests.get("https://habr.com/ru/rss/best/daily/?fl=ru")
    parser = Parser(xml=xml.content, limit=1)
    feed = parser.parse()
    item = feed.feed[0]
    return (item.title, extract_data(item.description))

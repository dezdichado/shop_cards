import lxml.html
from typing import Tuple
from urllib.parse import urljoin


def get_shop_urls(html):
    tree = lxml.html.fromstring(html)
    tags = tree.xpath("body/form/table/tr[3]/td/span[1]/table[2]/tr/td/li/a")
    return [urljoin("https://toshop.ru/", tag.get("href")) for tag in tags]


def get_shop_coordinates(html) -> Tuple[float, float]:
    tree = lxml.html.fromstring(html)
    tag = tree.xpath('//*[@id="lblBlockMain"]/div[3]')[0]
    lat = float(tree.xpath('//meta[@itemprop="latitude"]')[0].get("content"))
    long = float(tree.xpath('//meta[@itemprop="longitude"]')[0].get("content"))
    return lat, long

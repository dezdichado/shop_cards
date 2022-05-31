import asyncio
import sys
sys.path.append("/Users/ilya/PycharmProjects/shop_cards/app")
sys.path.append("~/webapps/shop_cards/app")
from aiohttp import ClientSession, ClientError, TCPConnector, ClientResponse
import sqlite3
from user_agent import generate_user_agent
from crawler import parse


async def get_response(url: str, session: ClientSession) -> ClientResponse:
    for i in range(15):
        try:
            async with session.get(url, ssl=False,
                             headers={"User-Agent": generate_user_agent()}) as response:
                await response.read()
                return response
        except ClientError as e:
            if i == 14:
                print(f"Unable to get {url}: {e}")
                raise


async def get_chain_shops(chain_id: int, external_id: int):
    print(f"Getting chain {chain_id}")
    connector = TCPConnector(force_close=True)
    async with ClientSession(connector=connector,
                             raise_for_status=True) as session:
        resp = await get_response(f"https://toshop.ru/shops.aspx?NetID={external_id}&CityID=1351", session)
        html = await resp.text()
        urls = parse.get_shop_urls(html)
        shops = []
        for url in urls:
            print(f"Getting shop {urls.index(url) + 1} out of {len(urls)}")
            shop_id = int(url[url.rfind("=") + 1:])
            shop_resp = await get_response(url, session)
            shop_html = await shop_resp.text()
            latitude, longitude = parse.get_shop_coordinates(shop_html)
            shops.append((shop_id, chain_id, latitude, longitude))
    return shops


async def update_stores(db_filename):
    connection = sqlite3.connect(db_filename)
    cursor = connection.cursor()
    cursor.execute("SELECT id, external_id FROM storechain WHERE is_active=true;")
    chain_ids = cursor.fetchall()
    cursor.execute("DELETE FROM store;")
    for chain_id, external_id in chain_ids:
        shops = await get_chain_shops(chain_id, external_id)
        cursor.executemany("INSERT INTO store (id, store_chain_id, latitude, longitude) VALUES (?, ?, ?, ?);", shops)
    connection.commit()
    connection.close()

asyncio.run(update_stores("sql_app.db"))

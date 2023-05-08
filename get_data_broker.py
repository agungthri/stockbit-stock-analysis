import aiohttp
import asyncio
import orjson
import itertools
import os
import pandas as pd
import logging
from typing import List, Tuple
from aiohttp import ClientSession
from get_codes import get_codes
from get_date_list import get_date_list
from urllib.parse import urlencode
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()


BASE_BROKER_URL = "https://exodus.stockbit.com/marketdetectors/{}"
AUTH_TOKEN = os.getenv('AUTH')
HEADERS = {"Authorization":AUTH_TOKEN}
FROM = "2022-05-03"
TO = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
PARAMS  = {
  'transaction_type': 'TRANSACTION_TYPE_NET',
  'market_board': 'MARKET_BOARD_REGULER',
  'investor_type': 'INVESTOR_TYPE_ALL'
}


async def get_data(session, url):
    async with session.get(url) as response:
        data = await response.read()
        return orjson.loads(data)


async def get_broker_data(data, date):
    data_buy = data['data']['broker_summary']['brokers_buy']
    data_sell = data['data']['broker_summary']['brokers_sell']
    data_buy = pd.DataFrame(data_buy)[['blot', 'netbs_broker_code']].rename(columns={'blot': date})
    data_sell = pd.DataFrame(data_sell)[['slot', 'netbs_broker_code']].rename(columns={'slot': date})
    data = pd.concat([data_buy, data_sell])
    data[date] = pd.to_numeric(data[date])
    data.set_index("netbs_broker_code", inplace=True)
    return data
    

def save_data(data, code, date):
    data.to_pickle(f"data/broker/{code}-{date}.pkl")
    print(f"{code}-{date}-Download... ")


async def process_data(code, date, data):
    data = await get_broker_data(data, date)
    save_data(data, code, date)


async def download_data(session, url, code, date):
    try:
        data = await get_data(session, url)
        await process_data(code, date, data)
    except Exception as e:
        pass
        print(f"{code}-{date}-{e}")


async def get_connector(limit: int):
    return aiohttp.TCPConnector(limit=limit)


async def get_session(connector, headers):
    async with aiohttp.ClientSession(connector=connector, headers=headers) as session:
        yield session


def get_existing_files() -> set:
    return set(os.listdir("data/broker"))


def create_task(session: ClientSession, code: str, date: str) -> asyncio.Task:
    PARAMS['from'] = date
    PARAMS['to'] = date
    URL = BASE_BROKER_URL.format(code) + "?" + urlencode(PARAMS)
    return asyncio.create_task(download_data(session, URL, code, date))


def create_tasks(session: ClientSession, codes: List[str], date_range: List[str]) -> List[asyncio.Task]:
    existing_files = get_existing_files()
    tasks = [create_task(session, code, date) for code, date in itertools.product(codes, date_range) if f"{code}-{date}.pkl" not in existing_files]
    return tasks


async def run_tasks(tasks):
    await asyncio.gather(*tasks)


async def main(code):
    connector = await get_connector(limit=5)
    async for session in get_session(connector=connector, headers=HEADERS):
        tasks = create_tasks(session, [code], get_date_list(FROM, TO))
        await run_tasks(tasks)




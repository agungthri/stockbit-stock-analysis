import asyncio
import aiohttp
import os
from dotenv import load_dotenv
from execute_time import timing_async

from get_codes import get_codes
from urllib.parse import urlencode, urlparse, parse_qs
import itertools

load_dotenv()

AUTH_TOKEN = os.environ.get('AUTH')
DATA_DIR  = "data"
HEADERS = {"Authorization": AUTH_TOKEN}
MAX_CONCURRENT_REQUESTS = 50
CODES = get_codes()
FINANCIAL_URL = "https://exodus.stockbit.com/findata-view/company/financial?"
REPORT_TYPES = {
    'income_statement': 1,
    'balance_sheet': 2,
    'cash_flow': 3
}


REV_REPORT_TYPES = {val: key for key, val in REPORT_TYPES.items()}


def generate_financials_urls():
    params = [{'symbol': code, 'data_type': 1, 'report_type': REPORT_TYPES[report_type], 'statement_type': 1}
              for code, report_type in itertools.product(CODES, REPORT_TYPES)]
    urls = [FINANCIAL_URL + urlencode(p) for p in params]
    return urls


async def parse_query_params(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    code = query_params['symbol'][0]
    report_type = int(query_params['report_type'][0])
    return code, report_type


async def fetch_data(session, url, headers):
    async with session.get(url, headers=headers) as response:
        data = await response.json()
        print(url)
        return data['data']['html_report']


def save_data_to_file(data, code, report_type):
    with open(f"{DATA_DIR}/{code}_{REV_REPORT_TYPES[report_type]}.html", 'w', encoding='utf-8') as f:
        f.write(data)


async def fetch_and_save(session, url, headers):
    code, report_type = await parse_query_params(url)
    data = await fetch_data(session, url, headers)
    save_data_to_file(data, code, report_type)
    print(url)


@timing_async
async def fetch_all(urls, headers):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            task = asyncio.ensure_future(fetch_data(session, url, headers))
            tasks.append(task)
        await asyncio.gather(*tasks)


loop = asyncio.get_event_loop()
results = loop.run_until_complete(fetch_all(generate_financials_urls(), HEADERS))







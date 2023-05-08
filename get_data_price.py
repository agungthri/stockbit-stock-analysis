import aiohttp
import asyncio
import os
from typing import List

from dotenv import load_dotenv
from execute_time import timing_async
from manage_data import to_save
from get_price_urls import get_price_urls
from get_codes import get_codes

load_dotenv()

AUTH_TOKEN = os.environ.get('AUTH')
DATA_DIR  = "data"
HEADERS = {"Authorization": AUTH_TOKEN}
MAX_CONCURRENT_REQUESTS = 50
CODES = get_codes()


async def fetch(session: aiohttp.ClientSession, semaphore: asyncio.Semaphore, url: str, code: str):
    """
    Fetch data from API using aiohttp and save it to file using to_save function
    :param session: aiohttp ClientSession
    :param semaphore: asyncio Semaphore to limit the number of concurrent requests
    :param url: URL to fetch data from
    :param code: stock code used for naming the file to save data
    """
    async with semaphore:
        async with session.get(url, headers=HEADERS) as response:
            data = await response.json()
            to_save(data['data']['chartbit'], code)


async def fetch_all(urls: List[str], codes: List[str]):
    """
    Run the fetch coroutine concurrently for all the URLs and codes.
    :param urls: list of URLs to fetch data from
    :param codes: list of stock codes used for naming the files to save data
    """
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url, code in zip(urls, codes):
            task = asyncio.ensure_future(fetch(session, semaphore, url, code))
            tasks.append(task)
        await asyncio.gather(*tasks)


@timing_async
async def main():
    """
    Main function that gets called when the script is run.
    It retrieves all the stock codes, gets the URLs for fetching data, and calls fetch_all to start the requests.
    """
    urls = [get_price_urls(code) for code in CODES]
    await fetch_all(urls, CODES)


if __name__ == "__main__":
    main_loop = asyncio.get_event_loop()
    main_loop.run_until_complete(main())

from urllib.parse import urlencode
from dotenv import load_dotenv
from datetime import datetime
import os
load_dotenv()

BASE_URL = os.environ.get('BASE_URL')
NOW_DATE = datetime.today().strftime('%Y-%m-%d')

def get_price_urls(ticker: str) -> str:
    params = {"to":"2000-01-01", "from":NOW_DATE, "limit":0}
    return BASE_URL.format(ticker) + "?" + urlencode(params)


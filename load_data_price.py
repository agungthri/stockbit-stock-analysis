import concurrent.futures
import pandas as pd
from get_codes import get_codes
from manage_data import to_load
from execute_time import timing_sync
from itertools import repeat

WINDOW = 300
PRICE  = 100
VALUE  = 100_000_000

def is_data_valid(data: pd.DataFrame) -> bool:
    if data.shape[0] < WINDOW:
        return False
    if data['close'].iloc[0] < PRICE:
        return False
    if data['value'].iloc[0] < VALUE:
        return False
    return True

def preprocess_data(data: pd.DataFrame, column:str, code:str) -> pd.Series:
    data = data.iloc[:WINDOW].set_index('date')#.assign(date=pd.to_datetime(data['date']))
    data = data[column].rolling(window=20).mean()
    return data.rename(code) / data.max()

def load_single_code_data(code: str, column: str) -> dict | None:
    data = to_load(code)
    return preprocess_data(data, column, code) if is_data_valid(data) else None

@timing_sync 
def load_data(column: str = 'close') -> list:
    codes = get_codes()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(load_single_code_data, codes, repeat(column, len(codes)))
    return [result for result in results if result is not None]



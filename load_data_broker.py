import os
import pandas as pd
import asyncio
from get_data_broker import main

def get_all_data(code):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(code))

    all_data = []
    for i in os.listdir('data/broker'):
        if code in i:
            all_data.append(pd.read_pickle("data/broker/" + i))

    return pd.concat(all_data, axis=1)

def process_data(data):
    data = data.cumsum(axis=1)
    return data

def save_to_excel(data):
    data.to_excel("broker-summary-result.xlsx")

if __name__ == '__main__':
    code = 'PGAS'
    all_data = get_all_data(code)
    processed_data = process_data(all_data)
    save_to_excel(processed_data)

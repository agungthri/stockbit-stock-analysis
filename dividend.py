import pandas as pd
from get_codes import get_codes
from manage_data import to_load


def load_data(code):
    data = to_load(code)
    data = data[data['dividend'] != 0]
    data['month'] = pd.to_datetime(data['date']).dt.month
    data['year'] = pd.to_datetime(data['date']).dt.year
    data = data.set_index('date')
    data['code'] = code
    data['yield'] = data['dividend'] / data['close']
    return data[['close', 'dividend', 'month', 'year', 'code', 'yield']]


def combine_data():
    all_data_list = [load_data(code) for code in get_codes()]
    all_dataframe = pd.concat(all_data_list)
    return all_dataframe


def save_to_excel(dataframe):
    dataframe.to_excel('dividend.xlsx')


def main():
    all_data = combine_data()
    save_to_excel(all_data)
    print('Done.')


if __name__ == '__main__':
    main()

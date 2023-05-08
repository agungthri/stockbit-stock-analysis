from load_data_price import load_data
import pandas as pd

def get_correlation_data(code, column):
    data = pd.concat(load_data(column), axis=1).corr()
    return data[code].sort_values(ascending=False)

def save_to_excel(data, filename):
    pd.concat([data.head(10), data.tail(10)]).to_excel(filename)

if __name__ == '__main__':
    code = 'BBRI'
    column = 'close'
    correlation_data = get_correlation_data(code, column)
    save_to_excel(correlation_data, 'correlation-without-lag-result.xlsx')
    print('done...')

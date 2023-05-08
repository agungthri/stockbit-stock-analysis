import pandas as pd

data_path = 'data/{}-price.pickle'

def to_save(data, code):
    data = pd.DataFrame(data)
    data.to_pickle(data_path.format(code))

def to_load(code):
    return pd.read_pickle(data_path.format(code))
